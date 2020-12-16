
'''
Create figure describing simulation methods for nonuniform data.
'''

import os,unipath
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import iwtspm as iws

plt.style.use('bmh')
mpl.rcParams['xtick.labelsize'] = 'small'
mpl.rcParams['ytick.labelsize'] = 'small'
mpl.rcParams['font.sans-serif'] = 'Arial'


def generate_dataset_multipulse():
	y0,y1 = iws.random.generate_dataset(J, Q, sig_amp=0, sig_width=sig_width, dist='gauss_matern', distparams=(s,w))
	sig   = iws.signal.multi_pulse(Q=101, q=[20, 50, 80], w=pwidth)
	y1    = y1 + sig
	return y0,y1



#(0) Run a single iteration:
np.random.seed(3)
wd          = os.path.join( os.path.dirname( __file__ ) , '_wd' )
### set baseline parameters:
Q           = 101
J           = 20
sig_amp     = 1
sig_width   = 40
sd          = 1
sd_ratio    = 1
fwhm        = 20
fwhm_ratio  = 1
pwidth      = 10
run_tests   = True
### construct simulation objects:
s           = iws.signal.sigmoid_pulse_amps( Q=Q, q0=50, w=sig_width, wfall=5, amp0=(sd*sd_ratio), amp1=sd )
w           = iws.signal.sigmoid_pulse_amps( Q=Q, q0=50, w=sig_width, wfall=5, amp0=(fwhm*fwhm_ratio), amp1=fwhm)
gen         = generate_dataset_multipulse
if run_tests:
	sim         = iws.sim.Simulator(wd, gen, suff='')
	sim.clear_wd()
	p0,p1,p2,p3 = sim.run_iteration()
	y0,y1       = sim.get_data()
else:
	y0,y1   = gen()
### plot:
plt.close('all')
fig,AX = plt.subplots( 1, 2, figsize=(8,3) )
plt.get_current_fig_manager().window.move(0, 0)
ax0,ax1 = AX.flatten()
### plot dataset:
q   = np.linspace(0, 1, Q)
ax0.plot(q,  y0.T, 'k', lw=0.3 )
ax0.plot(q,  y1.T, 'r', lw=0.3 )
ax0.plot(q, y0.mean(axis=0), 'k', lw=5, label='Mean A' )
ax0.plot(q, y1.mean(axis=0), 'r', lw=5, label='Mean B' )
ax0.legend()

### plot p curves
if run_tests:
	ax1.plot(q, p0, '0.7', lw=3, label='Unadjusted')
	ax1.plot(q, p1, 'b', label='IWT')
	ax1.plot(q, p2, 'c', label='SPM')
	ax1.plot(q, p3, 'm', label='SnPM')
	ax1.axhline(0.05, color='k', linestyle='--')
	ax1.set_ylim(-0.05, 1.05)
	ax1.set_ylabel( 'Probability' )
	ax1.legend()
plt.tight_layout()
plt.show()


dirREPO       = unipath.Path( os.path.dirname(__file__) ).parent.parent
fname_fig     = os.path.join( dirREPO, 'Figures', 'Simulation', 'fig_multipulse.pdf')
plt.savefig(fname_fig)