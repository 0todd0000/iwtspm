

import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import iwtspm as iws




plt.style.use('bmh')
mpl.rcParams['xtick.labelsize'] = 'small'
mpl.rcParams['ytick.labelsize'] = 'small'
mpl.rcParams['font.sans-serif'] = 'Arial'


colors        = ['0.7', 'b', 'c', 'm']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)



wd            = '/Users/todd/Desktop/Working/'
simname       = 'samplesize'
simname       = 'unbalanced'
# simname       = 'signalwidth'
# simname       = 'fwhm'
# simname       = 'fwhmratio'
# simname       = 'sdratio'
# simname       = 'unequalvar'
# simname       = 'multipulsewidth'

fname_results = os.path.join(wd, simname, '_results.npz')



plt.close('all')
iws.perf.plot_performance_results( fname_results, uxtransform=None )
plt.show()




# fnamePDF   = os.path.join(dir0, 'results', f'fig-{suffix}.pdf')
# plt.savefig( fnamePDF )

