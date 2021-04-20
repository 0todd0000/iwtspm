
import os,unipath
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import iwtspm as iws

plt.style.use('bmh')
mpl.rcParams['xtick.labelsize'] = 'small'
mpl.rcParams['ytick.labelsize'] = 'small'
mpl.rcParams['font.sans-serif'] = 'Arial'
colors = ['0.7', 'm', 'b', 'c']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)



dirREPO        = unipath.Path( os.path.dirname(__file__) ).parent.parent
dir0           = os.path.join( dirREPO, 'Data', 'Simulation')
perf_variable  = 'FPR'
perf_variable  = 'Sensitivity'



perf_variables = 'FPR', 'Sensitivity'
perfvarind     = perf_variables.index(perf_variable)
simnames       = []
simnames.append( ['samplesize', 'unbalanced'] )
simnames.append( ['signalamp', 'signalwidth', 'multipulsewidth'] )
simnames.append( ['fwhm', 'fwhmratio'] )
simnames.append( ['sdratio', 'unequalvar', 'skew'] )

simlabels      = []
d0,d1          = r'$\mathcal{D}_0$', r'$\mathcal{D}_1$'
simlabels.append( ['Sample size', 'Imbalance'] )
simlabels.append( ['Signal amplitude', 'Signal width', 'Multi-pulse signal widths'] )
simlabels.append( ['FWHM', 'FWHM ratio'] )
simlabels.append( [r'SD ratio  (%s : %s)'%(d0,d1), 'SD ratio  (Group A : B)', 'Skewness'] )

rowlabels      = ['Sample', 'Signal', 'Smoothness', 'Variance']


plt.close('all')
fig,AX = plt.subplots( 4, 3, figsize=(12,12) )
plt.get_current_fig_manager().window.move(0, 0)

n              = 0
for i,rowsimnames in enumerate(simnames):
	for ii,simname in enumerate(rowsimnames):
		fname_results   = os.path.join(dir0, simname, '_results.npz')
		ux,perf,blvalue = iws.perf.load_sim_results(fname_results, alpha=0.05)
		ax              = AX[i,ii]
		
		yperf  = perf[:,:,perfvarind]
		if simname == 'signalamp':
			ux,yperf = ux[1:], yperf[1:]
		
		if simname in ['fwhmratio', 'sdratio', 'unequalvar']:
			uxs = ['1/5', '1/4', '1/3', '1/2', 1, 2, 3, 4, 5] 
			ux  = [-3, -2, -1, 0, 1, 2, 3, 4, 5]
			ax.plot( ux, yperf )
			plt.setp(ax, xticks=ux, xticklabels=uxs)
		else:
			ax.plot( ux, yperf )

		blvalue = 0 if simname=='skew' else blvalue
		if blvalue is not None:
			ax.axvline( blvalue, color='k', ls='--')
		
		ax.set_xlabel( simlabels[i][ii] )
		ax.text(0.03, 0.92, '(%s)'%chr(97+n), transform=ax.transAxes)
		n+=1
		
plt.setp(AX, ylim=(-0.05,1))
[ax.set_visible(False)  for ax in [AX[0,2],AX[2,2]]]
[ax.set_ylabel(perf_variable)   for ax in AX[:,0]]

ax = AX[0,0]
labels = ['Unadjusted', 'IWT', 'SPM', 'SnPM', 'Baseline value']
fig.legend(ax.lines, labels, loc='lower center', bbox_to_anchor=(0.5,0.97), ncol=5)


plt.tight_layout(rect=[0,0,1,0.97])
plt.show()


