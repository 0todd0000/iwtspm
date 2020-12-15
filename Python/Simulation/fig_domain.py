
'''
Create figure describing domain definition for simulation results.
'''

import os,unipath


from math import floor
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
# import power1d
import iwtspm as iws

plt.style.use('bmh')
mpl.rcParams['xtick.labelsize'] = 'small'
mpl.rcParams['ytick.labelsize'] = 'small'
mpl.rcParams['font.sans-serif'] = 'Arial'


Q     = 101
amp   = 1
q0    = 50
w     = 20
wfall = 5

# q0       = int( floor( 50 - 0.5 * w ) )
# q1       = q0 + w

# a        = 0.5 * amp
# signal1a = power1d.geom.Sigmoid(Q, q0=q0-w, q1=q0, x0=-a, x1=a)
# signal1b = power1d.geom.Sigmoid(Q, q0=q1, q1=q1+w, x0=a, x1=-a)
# y1a,y1b  = signal1a.toarray(), signal1b.toarray()
# y        = y1a + y1b


y        = iws.signal.sigmoid_pulse(Q, q0=q0, w=w, wfall=wfall, amp=amp)


plt.close('all')
plt.figure(figsize=(5,3))
plt.get_current_fig_manager().window.move(0, 0)
ax = plt.axes()
q  = np.linspace(0, 1, Q)
ax.plot(q, np.zeros(Q), color='0.6', lw=7, label=r'$\mu_0$')
ax.plot(q, y, color='k', lw=3, label=r'$\mu_1$')
ax.legend(loc='lower right', bbox_to_anchor=(0.98, 0.1))

q00,q01  = 0.01 * np.array([q0 - 0.5*w , q0 + 0.5*w])
q10,q11  = 0.01 * np.array([100*q00 - wfall, 100*q01 + wfall])

ax.vlines([q00,q01], 0, 1, color='r', linestyle='--', lw=1)
ax.vlines([q10,q11], 0, 1, color='b', linestyle='--', lw=1)

ax.text(0.8, 0.5, r'$D_0$', color='b', ha='center')
ax.text(0.2, 0.5, r'$D_0$', color='b', ha='center')
ax.text(0.5, 0.6, r'$D_1$', color='b', ha='center')
ax.plot([0, q10], [0.48]*2, color='b', lw=2)
ax.plot([q11, 1], [0.48]*2, color='b', lw=2)
ax.plot([q10,q11], [0.58]*2, color='b', lw=2)

ax.set_xlabel('Domain position')
plt.tight_layout()
plt.show()




dirREPO       = unipath.Path( os.path.dirname(__file__) ).parent.parent
fname_fig     = os.path.join( dirREPO, 'Figures', 'Simulation', 'fig_domain.pdf')
plt.savefig(fname_fig)