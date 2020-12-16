
'''
Estimate smoothness (FWHM) for all experimental datasets.
'''



import os,unipath
from math import log
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
eps = np.finfo(np.float).eps
import spm1d

plt.style.use('bmh')
mpl.rcParams['xtick.labelsize'] = 'small'
mpl.rcParams['ytick.labelsize'] = 'small'
mpl.rcParams['font.sans-serif'] = 'Arial'


def load_csv(fnameCSV):
	a             = np.loadtxt(fname_data, delimiter=',')
	group         = a[:,0]
	y             = a[:,1:]
	u             = np.unique(group)
	y0,y1         = y[group==u[0]], y[group==u[1]]
	return y0,y1


# Estimate non-normality for all datasets:
dirREPO           = unipath.Path( os.path.dirname(__file__) ).parent.parent
dataset_labels    = ['Kautz1991a', 'Kautz1991b', 'Neptune1999', 'Besier2009a', 'Besier2009b', 'Dorn2012']
spms              = []
for dataset_label in dataset_labels:
	fname_data    = os.path.join( dirREPO, 'Data', 'ExperimentalData', '%s.csv' %dataset_label)
	y0,y1         = load_csv(fname_data)
	spmi          = spm1d.stats.normality.k2.ttest2(y0, y1).inference(0.05)
	spms.append( spmi )



plt.close('all')
fig,AX = plt.subplots(2, 3, figsize=(10,5) )
plt.get_current_fig_manager().window.move(0, 0)
for i,(ax,spm) in enumerate( zip(AX.flatten(), spms) ):
	k2 = spm.z
	x  = np.linspace(0, 1, k2.size)
	ax.plot(x, k2)
	ax.text( 0.05, 0.92, '(%s)  %s' %(chr(97+i), dataset_labels[i]),  transform=ax.transAxes  )

plt.setp(AX, ylim=(0, 60))
[ax.set_ylabel(f'K2 value')  for ax in AX[:,0]]
plt.setp(AX[:,1:], yticklabels=[])
plt.tight_layout()
plt.show()



fname_fig     = os.path.join( dirREPO, 'Figures', 'ExperimentalData', 'fig_normality.pdf')
plt.savefig(fname_fig)