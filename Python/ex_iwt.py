
'''
Example IWT analysis in Python via Rscript
'''



import os,unipath
import numpy as np
from matplotlib import pyplot as plt



def run_test_iwt(niter=1000, seed=0):
	# fnameR       = os.path.join(dir0, 'myscript.R')
	fnameR       = '/Users/todd/GitHub/-DomainMethodComparison/_Development/Analyses2020-10-26/R/run_iwt_two_tailed.R'
	# fnameR       = os.path.join( os.path.dirname(__file__) , 'run_iwt_two_tailed.R' )
	
	p_iwt        = np.loadtxt(fname_iwt_results, delimiter=',')
	return p_iwt
	


# Specify file names and parameters:
dirREPO       = unipath.Path( os.path.dirname(__file__) ).parent
fname_Rscript = os.path.join( dirREPO, 'R', 'run_iwt_two_tailed.R')
fname_data    = os.path.join( dirREPO, 'R', 'data.csv')
fname_results = os.path.join( dirREPO, 'R', 'iwt.csv')
seed          = 1     # rng seed
niter         = 1000  # number of IWT iterations
ngroupA       = 10    # number of observations (rows) in Group A


# Run analyses
os.system( f'Rscript {fname_Rscript} {seed} {niter} {ngroupA} {fname_data} {fname_results}' )
p_iwt        = np.loadtxt(fname_results, delimiter=',')


# Plot results:
plt.close('all')
plt.figure()
ax = plt.axes()
ax.plot(p_iwt)
plt.show()
