
'''
Estimate smoothness (FWHM) for all experimental datasets.
'''



import os,unipath
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

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


# Estimate FWHM for all datasets:
dirREPO           = unipath.Path( os.path.dirname(__file__) ).parent.parent
dataset_labels    = ['Kautz1991a', 'Kautz1991b', 'Neptune1999', 'Besier2009a', 'Besier2009b', 'Dorn2012']
sd                = []
for dataset_label in dataset_labels:
	fname_data    = os.path.join( dirREPO, 'Data', 'ExperimentalData', '%s.csv' %dataset_label)
	y0,y1         = load_csv(fname_data)
	s0,s1         = y0.std(axis=0, ddof=1), y1.std(axis=0, ddof=1)
	s             = np.sqrt(s0**2 + s1**2)
	s             = (s - s.min()) / (s.max()-s.min())
	sd.append( s )



plt.close('all')
plt.figure()
plt.get_current_fig_manager().window.move(0, 0)
ax = plt.axes()
for s in sd:
	x = np.linspace(0, 1, s.size)
	ax.plot(x, s)
ax.legend(dataset_labels)
ax.set_ylabel('Estimated standard deviation (relative)')
plt.tight_layout()
plt.show()


fname_fig     = os.path.join( dirREPO, 'Figures', 'ExperimentalData', 'fig_sd.pdf')
plt.savefig(fname_fig)