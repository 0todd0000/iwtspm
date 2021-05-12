
'''
Example IWT analysis in Python via Rscript

Experimental data
'''



import os
import numpy as np
from matplotlib import pyplot as plt
import iwtspm as iws



# Specify file names and parameters:
fname_Rscript = os.path.join( iws.dirREPO, 'R', 'run_iwt_two_tailed.R')
fname_data    = os.path.join( iws.dirREPO, 'Data', 'ExperimentalData', 'Kautz1991a.csv')
fname_results = os.path.join( iws.dirREPO, 'R', 'iwt.csv')
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
