
'''
Create figure describing domain definition for simulation results.
'''

import os
from math import floor
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import iwtspm as iws

plt.style.use('bmh')
mpl.rcParams['xtick.labelsize'] = 'small'
mpl.rcParams['ytick.labelsize'] = 'small'
mpl.rcParams['font.sans-serif'] = 'Arial'
mpl.rcParams["text.usetex"] = False


Q     = 101
amp   = 1
q0    = 50
w     = 40
wfall = 5
y     = iws.signal.sigmoid_pulse(Q, q0=q0, w=w, wfall=wfall, amp=amp)



plt.close('all')
c0    = '0.2'
c1    = '0.0'
c2    = '0.6'
plt.figure(figsize=(5,3))
plt.get_current_fig_manager().window.move(0, 0)
ax = plt.axes()
q  = np.linspace(0, 1, Q)
ax.plot(q, np.zeros(Q), color='0.6', lw=7, label=r'$\mu_A$')
ax.plot(q, y, color='k', lw=3, label=r'$\mu_B$')
ax.legend(loc='lower right', bbox_to_anchor=(0.98, 0.1))

q00,q01  = 0.01 * np.array([q0 - 0.5*w , q0 + 0.5*w])
q10,q11  = 0.01 * np.array([100*q00 - wfall, 100*q01 + wfall])

ax.vlines([q00,q01], 0, 1, color=c1, linestyle='--', lw=1)
ax.vlines([q10,q11], 0, 1, color=c0, linestyle='--', lw=1)

ax.text(0.8, 0.5, r'$\mathcal{D}_0$', color=c0, ha='center')
ax.text(0.2, 0.5, r'$\mathcal{D}_0$', color=c0, ha='center')
ax.text(0.5, 0.6, r'$\mathcal{D}_1$', color=c0, ha='center')
ax.text(0.5, 0.82, 'Signal width', color=c1, ha='center')
ax.text(-0.03, 0.92, 'Step width (0.05)', color=c2, va='center')
ax.text(0.77, 0.92, 'Step width (0.05)', color=c2, va='center')
ax.plot([0, q10], [0.48]*2, color=c0, lw=2)
ax.plot([q11, 1], [0.48]*2, color=c0, lw=2)
ax.plot([q10,q11], [0.58]*2, color=c0, lw=2)
ax.plot([q00,q01], [0.79]*2, color=c1, lw=2)
ax.plot([q00, q10], [0.92]*2, color=c2, lw=4)
ax.plot([q01, q11], [0.92]*2, color=c2, lw=4)
ax.set_xlabel('Domain position')
ax.set_facecolor('1.0')
ax.grid(False)
plt.tight_layout()
plt.show()



dirREPO       = iws.dirREPO
fname_fig     = os.path.join( dirREPO, 'Figures', 'Simulation', 'fig_domain.pdf')
plt.savefig(fname_fig)