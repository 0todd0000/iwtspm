
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

grayscale  = False
if grayscale:
	colors     = ['0.89', 'k', '0.0', '0.5'] if grayscale else ['0.7', 'r', 'g', 'b']
	markers    = ['o', 'o', 's', '^']
	markers    = ['', '', '', '']
	mfcs       = ['0.7', 'k', '0.0', '1.0']
	lss        = ['-', '-', '--', '--']
	lws        = [3, 2, 2, 1.5]
	plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors, marker=markers, mfc=mfcs, ls=lss, lw=lws)



#(0) Run a single iteration:
np.random.seed(2)
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
run_tests   = True
### construct simulation objects:
s           = iws.signal.sigmoid_pulse_amps( Q=Q, q0=50, w=sig_width, wfall=5, amp0=(sd*sd_ratio), amp1=sd )
w           = iws.signal.sigmoid_pulse_amps( Q=Q, q0=50, w=sig_width, wfall=5, amp0=(fwhm*fwhm_ratio), amp1=fwhm)
gen         = lambda: iws.random.generate_dataset(J, Q, sig_amp=sig_amp, sig_width=sig_width, dist='gauss_matern', distparams=(s,w))
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
c0,c1 = ('k','0.7') if grayscale else ('k','r')
ax0.plot(q,  y0.T, color=c0, lw=0.3 )
ax0.plot(q,  y1.T, color=c1, lw=0.5 )
ax0.plot(q, y0.mean(axis=0), color=c0, lw=5, label='Sample mean A' )
ax0.plot(q, y1.mean(axis=0), color=c1, lw=5, label='Sample mean B' )
ax0.legend(loc='lower left', bbox_to_anchor=(0.27, 0.01), facecolor='w')


### plot p curves
if run_tests:
	ax1.plot(q, p0, label='Unadjusted')
	ax1.plot(q, p1, label='IWT')
	ax1.plot(q, p2, label='SPM')
	ax1.plot(q, p3, label='SnPM')
	if grayscale:
		ax1.axhline(0.05, color='0.85', linestyle='-', lw=5, label=r'$\alpha = 0.05$', zorder=-1)
	else:
		ax1.axhline(0.05, color='k', linestyle='--', lw=1, label=r'$\alpha = 0.05$', zorder=-1)
	ax1.set_ylim(-0.05, 1.05)
	ax1.set_ylabel( 'Probability' )
	ax1.legend(loc='lower left', bbox_to_anchor=(0.32, 0.45), facecolor='w')
	

d0  = r'$\mathcal{D}_0$'
d1  = r'$\mathcal{D}_1$'
for ax in AX:
	ax.axvspan(0.25, 0.75, alpha=0.5, color='0.90')
	[ax.text(x, 0.93, s, ha='center', transform=ax.transAxes)  for x,s in zip([0.15, 0.5, 0.85], [d0,d1,d0] )]
	ax.set_facecolor('1.0')
	ax.grid(False)
	


plt.tight_layout()
plt.show()


dirREPO       = unipath.Path( os.path.dirname(__file__) ).parent.parent
dirFIG        = os.path.join( dirREPO, 'Figures', 'Simulation')
dirFIG        = os.path.join(dirFIG, 'bw') if grayscale else dirFIG
fname_fig     = os.path.join( dirFIG, 'fig_baseline.pdf')
plt.savefig(fname_fig)