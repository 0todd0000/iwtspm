
'''
Create figure describing simulation methods for nonuniform data.
'''

import os
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
	colors     = ['0.89', 'k', '0.0', '0.5']
	markers    = ['o', 'o', 's', '^']
	markers    = ['', '', '', '']
	mfcs       = ['0.7', 'k', '0.0', '1.0']
	lss        = ['-', '-', '--', '--']
	lws        = [3, 2, 2, 1.5]
	plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors, marker=markers, mfc=mfcs, ls=lss, lw=lws)
else:
	colors     = ['0.7', 'm', 'b', 'c', 'r']
	lws        = [4, 2, 2, 2, 2]
	lss        = ['-', '-', '-', '-', ':']
	plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors, ls=lss, lw=lws)





#(0) Run a single iteration:
np.random.seed(2)
run_tests   = True
wd          = os.path.join( os.path.dirname( __file__ ) , '_wd' )
params      = iws.sim.SimulationParameters()   # baseline parameters
sim         = iws.sim.Simulator(wd, params, suffix='')
if run_tests:
	sim.clear_wd()
	p0,p1,p2,p3 = sim.run_iteration()
	p4          = iws.perf.fdr_corrected_pvalues(p0, alpha=0.05)
	y0,y1       = sim.get_data()
else:
	y0,y1       = sim.random()
### plot:
plt.close('all')
fig,AX = plt.subplots( 1, 2, figsize=(8,3) )
plt.get_current_fig_manager().window.move(0, 0)
ax0,ax1 = AX.flatten()
### plot dataset:
q   = np.linspace(0, 1, params.Q)
cm0,cm1 = ('k','0.7') if grayscale else ('k','r')
c0,c1   = ('k','0.7') if grayscale else ('0.7', (1,0.5,0.5))

ax0.plot(q,  y0.T, color=c0, lw=0.5 )
ax0.plot(q,  y1.T, color=c1, lw=0.5 )
ax0.plot(q, y0.mean(axis=0), color=cm0, lw=3, label='Sample mean A' )
ax0.plot(q, y1.mean(axis=0), color=cm1, lw=3, label='Sample mean B' )
ax0.legend(loc='lower left', bbox_to_anchor=(0.27, 0.01), facecolor='w')


### plot p curves
if run_tests:
	ax1.plot(q, p0, label='Unadjusted')
	ax1.plot(q, p1, label='IWT')
	ax1.plot(q, p2, label='SPM')
	ax1.plot(q, p3, label='SnPM')
	ax1.plot(q, p4, label='FDR')
	if grayscale:
		ax1.axhline(0.05, color='0.85', linestyle='-', lw=5, label=r'$\alpha = 0.05$', zorder=-1)
	else:
		ax1.axhline(0.05, color='k', linestyle='--', lw=1, label=r'$\alpha = 0.05$', zorder=-1)
	ax1.set_ylim(-0.05, 1.05)
	ax1.set_ylabel( 'Probability' )
	ax1.legend(loc='lower left', bbox_to_anchor=(0.30, 0.40), facecolor='w')
	

d0  = r'$\mathcal{D}_0$'
d1  = r'$\mathcal{D}_1$'
for ax in AX:
	ax.axvspan(0.25, 0.75, alpha=0.5, color='0.90')
	[ax.text(x, 0.93, s, ha='center', transform=ax.transAxes)  for x,s in zip([0.15, 0.5, 0.85], [d0,d1,d0] )]
	ax.set_facecolor('1.0')
	ax.grid(False)
	


plt.tight_layout()
plt.show()


dirFIG        = os.path.join( iws.dirREPO, 'Figures', 'Simulation')
dirFIG        = os.path.join(dirFIG, 'bw') if grayscale else dirFIG
fname_fig     = os.path.join( dirFIG, 'fig_baseline.pdf')
plt.savefig(fname_fig)