
'''
Analyze all experimental datasets using three techniques:
1. IWT
2. SPM
3. SnPM   (permutation tests, using t_max)


Experimental data
'''



import os
import numpy as np
from scipy import stats
import matplotlib as mpl
from matplotlib import pyplot as plt
import spm1d
import iwtspm as iws


plt.style.use('bmh')
mpl.rcParams['xtick.labelsize'] = 'small'
mpl.rcParams['ytick.labelsize'] = 'small'
mpl.rcParams['font.sans-serif'] = 'Arial'


grayscale   = False

if grayscale:
	colorsM = ['k', '0.7']
	colors0 = ['k', '0.7']
	colors  = ['0.89', 'k', '0.0', '0.5', '0.5']
else:
	colorsM = ['k', 'c']
	colors0 = ['0.7', (0.5,1,1)]
	colors  = ['0.7', 'm', 'b', 'c', 'k']
lss         = ['-', '-', '--', '--', ':']
lws         = [3, 2, 2, 1.5, 1.5]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors, ls=lss, lw=lws)




def load_csv(fnameCSV):
	a            = np.loadtxt(fname_data, delimiter=',')
	group        = a[:,0]
	y            = a[:,1:]
	u            = np.unique(group)
	y0,y1        = y[group==u[0]], y[group==u[1]]
	return y0,y1


def calc_p_unadjusted(y0, y1):
	spm          = spm1d.stats.ttest2(y0, y1, equal_var=False)
	z,df         = spm.z, spm.df[1]
	p            = stats.f.sf(z**2, 1, df)
	return p


def calc_p_adjusted_spm(y0, y1):
	spm          = spm1d.stats.ttest2(y0, y1, equal_var=False)
	z,df         = spm.z, spm.df[1]
	p            = spm1d.rft1d.f.sf(z**2, (1,df), spm.Q, spm.fwhm, withBonf=True)
	return p


def calc_p_adjusted_snpm(y0, y1, niter=1000):
	n0,n1      = y0.shape[0], y1.shape[0]
	group      = [0]*n0 + [1]*n1
	y          = np.vstack([y0, y1])
	snpm       = spm1d.stats.nonparam.anova1(y, group)
	niter      = -1 if (niter > snpm.nPermUnique) else niter
	snpmi      = snpm.inference(iterations=niter)
	pdf        = np.abs( snpmi.PDF0 )
	p          = np.array([ (pdf > z).mean() for z in snpmi.z])
	return p


def calc_p_adjusted_iwt(fname_data, seed=1, niter=1000):
	fname_Rscript     = os.path.join( dirREPO, 'R', 'run_iwt_two_tailed.R')
	fname_iwt_results = os.path.join( os.path.curdir , 'temp_iwt_results.csv' )
	os.system( f'Rscript {fname_Rscript} {seed} {niter} {fname_data} {fname_iwt_results}' )
	p                 = np.loadtxt(fname_iwt_results, delimiter=',')
	os.remove( fname_iwt_results )
	return p


def plot_results(p_unadjusted, p_iwt, p_spm, p_snpm, p_fdr, dv_label=None):
	fig,AX  = plt.subplots( 1, 2, figsize=(8,3) )
	plt.get_current_fig_manager().window.move(0, 0)
	ax0,ax1 = AX.flatten()
	q       = np.linspace(0, 1, p_unadjusted.size)
	### plot dataset:
	ax0.plot( q, y0.T, color=colors0[0], ls='-', lw=0.5 )
	ax0.plot( q, y1.T, color=colors0[1], ls='-', lw=0.5 )
	ax0.plot( q, y0.mean(axis=0), color=colorsM[0], ls='-', lw=3, label='Mean A' )
	ax0.plot( q, y1.mean(axis=0), color=colorsM[1], ls='-', lw=3, label='Mean B' )
	ax0.legend(facecolor='w')
	if dv_label is not None:
		ax0.set_ylabel( dv_label )
	### plot p curves
	ax1.plot( q, p_unadjusted, label='Unadjusted')
	ax1.plot( q, p_iwt,  label='IWT')
	ax1.plot( q, p_spm,  label='SPM')
	ax1.plot( q, p_snpm, label='SnPM')
	ax1.plot( q, p_fdr,  label='FDR')
	ax1.axhline(0.05, color='0.85', linestyle='-', lw=5, label=r'$\alpha = 0.05$', zorder=-1)



	ax1.set_ylim(-0.05, 1.05)
	ax1.legend(facecolor='w')
	ax1.set_ylabel( 'Probability' )
	
	for ax in [ax0,ax1]:
		ax.set_facecolor('1.0')
		ax.grid(False)
	
	plt.tight_layout()



# # (0) Analyze one dataset:
# dataset_label      = 'Kautz1991a'
# dirREPO            = iws.dirREPO
# fname_data         = os.path.join( dirREPO, 'Data', 'ExperimentalData', '%s.csv' %dataset_label)
# y0,y1              = load_csv(fname_data)
# p_unadjusted       = calc_p_unadjusted(y0, y1)
# p_spm              = calc_p_adjusted_spm(y0, y1)
# p_snpm             = calc_p_adjusted_snpm(y0, y1)
# p_iwt              = calc_p_adjusted_iwt(fname_data, seed=1, niter=1000)
# p_fdr              = iws.perf.fdr_corrected_pvalues(p_unadjusted, alpha=0.05)
# # p_iwt = 0.5 * np.ones(y0.shape[1])
# plt.close('all')
# plot_results(p_unadjusted, p_iwt, p_spm, p_snpm, p_fdr, dv_label='Force (N)')
# plt.show()






# (1) Analyze all datasets (and save figures):
dirREPO           = iws.dirREPO
dataset_labels    = ['Kautz1991a', 'Kautz1991b', 'Neptune1999', 'Besier2009a', 'Besier2009b', 'Dorn2012']
dv_labels         = ['Normal pedal force (N)', 'Tangential pedal force (N)', 'Knee flexion (deg)', 'Semimembranosus force (N)', 'Medial gastrocnemius force (N)', 'Anterior ground reaction force (N)']
for dataset_label, dv_label in zip(dataset_labels, dv_labels):
	print( f'Processing {dataset_label}...')
	fname_data    = os.path.join( dirREPO, 'Data', 'ExperimentalData', '%s.csv' %dataset_label)
	if grayscale:
		fname_fig = os.path.join( dirREPO, 'Figures', 'ExperimentalData', 'bw', '%s.pdf' %dataset_label)
	else:
		fname_fig = os.path.join( dirREPO, 'Figures', 'ExperimentalData', 'color', '%s.pdf' %dataset_label)
	y0,y1         = load_csv(fname_data)
	p_unadjusted  = calc_p_unadjusted(y0, y1)
	p_spm         = calc_p_adjusted_spm(y0, y1)
	p_snpm        = calc_p_adjusted_snpm(y0, y1)
	p_iwt         = calc_p_adjusted_iwt(fname_data, seed=1, niter=1000)
	p_fdr         = iws.perf.fdr_corrected_pvalues(p_unadjusted, alpha=0.05)
	plt.close('all')
	plot_results(p_unadjusted, p_iwt, p_spm, p_snpm, p_fdr, dv_label=dv_label)
	plt.show()
	plt.savefig(fname_fig)


