
'''
Probability calculators for 1D data

Only a single test is implemented:
- two-sample (two-tailed) 

The following 1D probabilities can be calculated:
- Unadjusted  (typical probability for univariate 0D data)
- IWT (Interval Wise Testing)
- SPM (Statistical Parametric Mapping)
- SnPM (Statistical non-Parametric Mapping) (i.e., permutation tests)

See the manuscript for descriptions of these procedures
'''


import os
import numpy as np
from scipy import stats
import spm1d



def p_iwt(y0, y1, niter=1000, seed=1, fname_data=None, fname_results=None):
	y            = np.vstack([y0,y1])
	group        = [0]*y0.shape[0] + [1]*y1.shape[0]
	a            = np.vstack( [group, y.T] ).T
	np.savetxt(fname_data, a, delimiter=',', fmt='%.3f')
	fnameR       = os.path.join( os.path.dirname( __file__ ) , 'R', 'run_iwt_two_tailed.R')
	os.system( f'Rscript {fnameR} {seed} {niter} {fname_data} {fname_results}' )
	p            = np.loadtxt(fname_results, delimiter=',')
	return p


def p_spm(y0, y1):
	spm  = spm1d.stats.ttest2(y0, y1, equal_var=False)
	return spm1d.rft1d.f.sf(spm.z**2, spm.df, spm.Q, spm.fwhm, withBonf=True)


def p_snpm(y0, y1, niter=1000):
	snpm       = spm1d.stats.nonparam.ttest2(y0, y1)
	niter      = -1 if (niter > snpm.nPermUnique) else niter
	snpmi      = snpm.inference(iterations=niter)
	pdf        = np.abs(snpmi.PDF0)
	p          = np.array([ (pdf > z).mean() for z in np.abs(snpmi.z)])
	return p


def p_unadjusted(y0, y1):
	spm  = spm1d.stats.ttest2(y0, y1, equal_var=False)
	return stats.f.sf(spm.z**2, 1, spm.df[1])


	