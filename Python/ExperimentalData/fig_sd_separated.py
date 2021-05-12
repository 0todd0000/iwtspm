
'''
Estimate smoothness (FWHM) for all experimental datasets.
'''



import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import iwtspm as iws


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
dirREPO           = iws.dirREPO
dataset_labels    = ['Kautz1991a', 'Kautz1991b', 'Neptune1999', 'Besier2009a', 'Besier2009b', 'Dorn2012']
unitstrs          = ['N', 'N', 'deg',     'N', 'N', 'N']
sd0,sd1,sdp       = [],[],[]  # Group 0, Group 1, Pooled standard deviations
for dataset_label in dataset_labels:
	fname_data    = os.path.join( dirREPO, 'Data', 'ExperimentalData', '%s.csv' %dataset_label)
	y0,y1         = load_csv(fname_data)
	s0,s1         = y0.std(axis=0, ddof=1), y1.std(axis=0, ddof=1)
	n0,n1         = y0.shape[0], y1.shape[0]
	s             = np.sqrt(  ((n0-1)*s0**2  + (n1-1)*s1**2) / (n0+n1-2)  )
	# s             = np.sqrt(s0**2 + s1**2)
	# s             = (s - s.min()) / (s.max()-s.min())
	sd0.append( s0 )
	sd1.append( s1 )
	sdp.append( s )



plt.close('all')
fig,AX = plt.subplots(2, 3, figsize=(10,5) )
plt.get_current_fig_manager().window.move(0, 0)
for i,(ax,s0,s1,sp) in enumerate( zip(AX.flatten(), sd0,sd1,sdp) ):
	x = np.linspace(0, 1, sp.size)
	h0 = ax.plot(x, s0, color='0.5', lw=0.5)[0]
	h1 = ax.plot(x, s1, color='0.5', lw=0.5)[0]
	hp = ax.plot(x, sp, color='0.0', lw=2)[0]
	
	ax.text( 0.05, 0.92, '(%s)  %s' %(chr(97+i), dataset_labels[i]),  transform=ax.transAxes  )
	ax.set_ylabel(f'SD  ({unitstrs[i]})')
	ax.set_facecolor('1.0')
	ax.grid(False)
	

AX[0,0].legend([h0,hp], ['Sample', 'Pooled'])

AX[0,1].set_ylim(0, 60)
AX[1,0].set_ylim(30, 420)
AX[1,2].set_ylim(0, 140)
plt.tight_layout()
plt.show()


fname_fig     = os.path.join( dirREPO, 'Figures', 'ExperimentalData', 'fig_sd_separated.pdf')
plt.savefig(fname_fig)