
'''
Create figure describing simulation methods for nonuniform data.
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



#(0) Run a single iteration:
np.random.seed(1)
### set baseline parameters:
Q           = 101
J           = 500
sig_amp     = 0
sig_width   = 40
sd          = 1
sd_ratio    = 1
fwhm        = 20
fwhm_ratio  = 1
skew        = 5
### construct simulation objects:
gen         = lambda : iws.rand.generate_dataset(Q, sample_sizes=(J,J), sig_amp=0, sig_width=sig_width, dist='skewed', distparams=(skew,))
y0,y1       = gen()
y           = np.vstack( [y0,y1] )
### plot:
plt.close('all')
fig,AX = plt.subplots( 1, 2, figsize=(8,3) )
plt.get_current_fig_manager().window.move(0, 0)
ax0,ax1 = AX.flatten()
### plot dataset:
q   = np.linspace(0, 1, Q)
ax0.plot(q,  y.T, lw=0.3 )
ax1.hist( y[:,50], color='0.7', alpha=0.8, bins=21 )
labels = ['(a)', '(b)  Distribution at position = 0.5']
[ax.text(0.06, 0.94, s, transform=ax.transAxes)   for ax,s in zip(AX,labels)]

ax0.set_ylim(-3.2, 3.2)
plt.tight_layout()
plt.show()



dirREPO       = iws.dirREPO
fname_fig     = os.path.join( dirREPO, 'Figures', 'Simulation', 'fig_skewed.pdf')
plt.savefig(fname_fig)