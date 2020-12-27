
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

colors     = ['0.89', 'k', '0.0', '0.5']
markers    = ['o', 'o', 's', '^']
markers    = ['', '', '', '']
mfcs       = ['0.7', 'k', '0.0', '1.0']
lss       = ['-', '-', '--', '--']
lws       = [3, 2, 2, 1.5]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors, marker=markers, mfc=mfcs, ls=lss, lw=lws)


#(0) Generate data to demonstrate simulation methods:
np.random.seed(2)
wd          = os.path.join( os.path.dirname( __file__ ) , '_wd' )
### set baseline parameters:
Q           = 101
J           = 20
e_type      = 'Gauss'
sig_amp     = 1
sig_width   = 40
sd          = 1
sd_ratio    = 1
fwhm        = 20
fwhm_ratio0 = 0.25
fwhm_ratio1 = 4
### construct simulation objects:
s           = iws.signal.sigmoid_pulse_amps( Q=Q, q0=50, w=sig_width, wfall=5, amp0=(sd*sd_ratio), amp1=sd )
w0          = iws.signal.sigmoid_pulse_amps( Q=Q, q0=50, w=sig_width, wfall=5, amp0=(fwhm*fwhm_ratio0), amp1=fwhm)
w1          = iws.signal.sigmoid_pulse_amps( Q=Q, q0=50, w=sig_width, wfall=5, amp0=(fwhm*fwhm_ratio1), amp1=fwhm)
gen0        = lambda: iws.random.generate_dataset(J, Q, sig_amp=sig_amp, sig_width=sig_width, dist='gauss_matern', distparams=(s,w0))
gen1        = lambda: iws.random.generate_dataset(J, Q, sig_amp=sig_amp, sig_width=sig_width, dist='gauss_matern', distparams=(s,w1))
yA0,yA1     = gen0()
yB0,yB1     = gen1()



#(1) Plot:
### plot:
plt.close('all')
fig,AX = plt.subplots( 1, 2, figsize=(8,3) )
plt.get_current_fig_manager().window.move(0, 0)
ax0,ax1 = AX.flatten()
### plot dataset:
q   = np.linspace(0, 1, Q)
d0  = r'$\mathcal{D}_0$'
d1  = r'$\mathcal{D}_1$'
for ax,y0,y1 in zip(AX, [yA0,yB0], [yA1,yB1]):
	ax.plot(q,  y0.T, 'k', ls='-', lw=0.3 )
	ax.plot(q,  y1.T, '0.85', ls='-', lw=0.5 )
	ax.plot(q, y0.mean(axis=0), 'k', lw=5, label='Sample mean A' )
	ax.plot(q, y1.mean(axis=0), '0.7', lw=5, label='Sample mean B' )
	
	ax.axvspan(0.25, 0.75, alpha=0.5, color='0.9')
	[ax.text(x, 0.93, s, ha='center', transform=ax.transAxes)  for x,s in zip([0.15, 0.5, 0.85], [d0,d1,d0] )]
	ax.set_facecolor('1.0')
	ax.grid(False)
	

ax0.legend(loc='lower center')
# ax0.legend(loc='lower left', bbox_to_anchor=(0.27, 0.01))
labels = [f'(a)  FWHM ratio = {fwhm_ratio0}', f'(b)  FWHM ratio = {fwhm_ratio1}']
[ax.text(0.06, 1.03, s, transform=ax.transAxes)   for ax,s in zip(AX,labels)]
plt.tight_layout()
plt.show()


dirREPO       = unipath.Path( os.path.dirname(__file__) ).parent.parent
fname_fig     = os.path.join( dirREPO, 'Figures', 'Simulation', 'fig_nonuniform-bw.pdf')
plt.savefig(fname_fig)




