
'''
Example IWT analysis in Python via Rscript

Experimental data
'''



import os,unipath
import numpy as np
from matplotlib import pyplot as plt



# Specify file names and parameters:
dirREPO       = unipath.Path( os.path.dirname(__file__) ).parent.parent
fname_Rscript = os.path.join( dirREPO, 'R', 'run_iwt_two_tailed.R')
fname_data    = os.path.join( dirREPO, 'Data', 'ExperimentalData', 'Kautz1991a.csv')
fname_results = os.path.join( dirREPO, 'R', 'iwt.csv')
seed          = 1     # rng seed
niter         = 1000  # number of IWT iterations


# Run analyses
os.system( f'Rscript {fname_Rscript} {seed} {niter} {fname_data} {fname_results}' )
p_iwt        = np.loadtxt(fname_results, delimiter=',')


# Plot results:
plt.close('all')
plt.figure()
ax = plt.axes()
ax.plot(p_iwt)
plt.show()
