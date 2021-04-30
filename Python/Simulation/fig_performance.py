
import os,unipath
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import iwtspm as iws


# ----- USER PARAMETERS --------
perf_variable  = 'FWER'          # perf_variable should be "FWER" or "Sensitivity"
# perf_variable  = 'Sensitivity'   # perf_variable should be "FWER" or "Sensitivity"
alpha          = 0.05            # Type I error rate
niter          = 1000            # number of simulation iterations (100 or 1000); use 100 for faster figure generation
# ----- END USER PARAMETERS ----







plt.style.use('bmh')
mpl.rcParams['xtick.labelsize'] = 'small'
mpl.rcParams['ytick.labelsize'] = 'small'
mpl.rcParams['font.sans-serif'] = 'Arial'
colors = ['0.7', 'm', 'b', 'c']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)


dirREPO        = '/Users/todd/GitHub/iwtspm/'
dir0           = os.path.join( dirREPO, 'Data', 'Simulation')


perf_variables = 'FWER', 'Sensitivity'
perfvarind     = perf_variables.index(perf_variable)
simnames       = []
simnames.append( ['samplesize', 'unbalanced'] )
simnames.append( ['signalamp', 'signalwidth', 'multipulsewidth'] )
simnames.append( ['fwhm', 'fwhmratio'] )
simnames.append( ['sdratio', 'unequalvar', 'skew'] )


simlabels      = []
d0,d1          = '$\mathcal{D}_0$', '$\mathcal{D}_1$'
sigd0,sigd1    = '$\sigma_{\mathcal{D}_0}$', '$\sigma_{\mathcal{D}_1}$'
fwhmd0,fwhmd1  = '$\mathrm{FWHM}_{\mathcal{D}_0}$', 'FWHM$_{\mathcal{D}_1}$'
simlabels.append( ['Sample size', r'Sample size imbalance ;   $N_{\mathrm{total}}=40$'] )
simlabels.append( ['Signal amplitude', 'Signal width', 'Multi-pulse signal widths'] )
simlabels.append( ['FWHM', r'FWHM ratio  (%s : %s) ;  %s$= 0.2$'%(d0,d1,fwhmd1)] )
simlabels.append( [r'$\sigma$  ratio  (%s : %s) ;  $\sigma_{\mathcal{D}_1} = 1$'%(sigd0,sigd1), r'$\sigma$  ratio  ( $\sigma_A$ : $\sigma_B$ ) ;  $\sigma_B = 1$', 'Skewness'] )

rowlabels      = ['Sample size', 'Signal', 'Smoothness', 'Variance']


plt.close('all')
fig,AX = plt.subplots( 4, 3, figsize=(12,12) )
plt.get_current_fig_manager().window.move(0, 0)

n              = 0
fname          = '_results100.npz' if niter==100 else '_results.npz'
for i,rowsimnames in enumerate(simnames):
	for ii,simname in enumerate(rowsimnames):
		fname_results   = os.path.join(dir0, simname, fname)
		ux,perf,perffdr,blvalue = iws.perf.load_sim_results(fname_results, alpha=0.05)
		ax              = AX[i,ii]
		
		yperf  = perf[:,:,perfvarind]
		yperffdr  = perffdr[:,perfvarind]
		if simname == 'signalamp':
			ux,yperf,yperffdr = ux[1:], yperf[1:], yperffdr[1:]
		
		if simname in ['fwhmratio', 'sdratio', 'unequalvar']:
			uxs = ['1/5', '1/4', '1/3', '1/2', 1, 2, 3, 4, 5] 
			ux  = [-3, -2, -1, 0, 1, 2, 3, 4, 5]
			ax.plot( ux, yperf )
			ax.plot( ux, yperffdr, color='r', ls=':' )
			plt.setp(ax, xticks=ux, xticklabels=uxs)
		else:
			if simname in ['signalwidth', 'multipulsewidth', 'fwhm']:
				ux = 0.01 * ux
			ax.plot( ux, yperf )
			ax.plot( ux, yperffdr, color='r', ls=':' )

		blvalue = 0 if simname=='skew' else blvalue
		if blvalue is not None:
			if simname in ['signalwidth', 'multipulsewidth', 'fwhm']:
				blvalue = 0.01 * blvalue
			ax.axvline( blvalue, color='k', ls='--')
		
		ax.set_xlabel( simlabels[i][ii] )
		ax.text(0.03, 0.92, '(%s)'%chr(97+n), transform=ax.transAxes)
		n+=1
		
if perf_variable == 'FWER':
	plt.setp(AX, ylim=(-0.05,0.4))
else:
	plt.setp(AX, ylim=(-0.05,1))
[ax.set_visible(False)  for ax in [AX[0,2],AX[2,2]]]
[ax.set_ylabel(perf_variable)   for ax in AX[:,0]]

ax = AX[0,0]
labels = ['Unadjusted', 'IWT', 'SPM', 'SnPM', 'FDR', 'Baseline value']
fig.legend(ax.lines, labels, loc='lower center', bbox_to_anchor=(0.5,0.97), ncol=6)

plt.tight_layout(rect=[0,0,0.97,0.97])


rowlabels = 'Sample', 'Signal', 'Smoothness', 'Variance'
rowlabely = [np.array( ax.get_position() )[:,1].mean()   for ax in AX[:,0]]
for y,label in zip(rowlabely, rowlabels):
	fig.text(0.97, y, label, rotation=-90, size=16, va='center')


plt.show()

