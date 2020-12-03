
'''
Estimate smoothness (FWHM) for all experimental datasets.
'''



import os,unipath
from math import log
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
eps = np.finfo(np.float).eps

plt.style.use('bmh')
mpl.rcParams['xtick.labelsize'] = 'small'
mpl.rcParams['ytick.labelsize'] = 'small'
mpl.rcParams['font.sans-serif'] = 'Arial'


def estimate_resels(R):
	ssq    = (R**2).sum(axis=0)
	### gradient estimation (Method 2)
	dy,dx  = np.gradient(R)
	v      = (dx**2).sum(axis=0)
	# normalize:
	v     /= (ssq + eps)
	# ignore zero-variance nodes:
	i      = np.isnan(v)
	v      = v[np.logical_not(i)]
	# global resels estimate:
	resels = np.sqrt(v / (4*log(2)))
	return resels

def estimate_fwhm(y0, y1, mean=True):
	r0,r1    = y0 - y0.mean(axis=0), y1 - y1.mean(axis=0)
	r        = np.vstack( [r0, r1] )
	resels   = estimate_resels(r)
	if mean:
		fwhm = 1 / resels.mean()
	else:
		fwhm = 1 / resels
	return fwhm

def load_csv(fnameCSV):
	a             = np.loadtxt(fname_data, delimiter=',')
	group         = a[:,0]
	y             = a[:,1:]
	u             = np.unique(group)
	y0,y1         = y[group==u[0]], y[group==u[1]]
	return y0,y1




# Estimate FWHM for all datasets:
dirREPO           = unipath.Path( os.path.dirname(__file__) ).parent.parent
dataset_labels    = ['Kautz1991a', 'Kautz1991b', 'Neptune1999', 'Besier2009a', 'Besier2009b', 'Dorn2012']
w                 = []
for dataset_label in dataset_labels:
	fname_data    = os.path.join( dirREPO, 'Data', 'ExperimentalData', '%s.csv' %dataset_label)
	y0,y1         = load_csv(fname_data)
	ww            = estimate_fwhm( y0 , y1, mean=False )
	w.append(ww)



plt.close('all')
plt.figure()
plt.get_current_fig_manager().window.move(0, 0)
ax = plt.axes()
for ww in w:
	x = np.linspace(0, 1, ww.size)
	ax.plot(x, ww)
ax.legend(dataset_labels)
ax.set_ylabel('Estimated smoothness (FWHM)')
plt.tight_layout()
plt.show()


fname_fig     = os.path.join( dirREPO, 'Figures', 'ExperimentalData', 'fig_smoothness.pdf')
plt.savefig(fname_fig)