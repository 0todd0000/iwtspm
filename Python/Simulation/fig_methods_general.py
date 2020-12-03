
'''
Create figure describing simulation methods for nonuniform data.
'''

import os,unipath
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import iwtspm as iws

plt.style.use('bmh')
mpl.rcParams['xtick.labelsize'] = 'small'
mpl.rcParams['ytick.labelsize'] = 'small'
mpl.rcParams['font.sans-serif'] = 'Arial'





#(0) Generate data to demonstrate simulation methods:
np.random.seed(1)
J,Q         = 10, 101

e0          = iws.random.gauss1dnu( J , Q , 5  * np.ones(Q) )
e1          = iws.random.gauss1dnu( J , Q , 30 * np.ones(Q) )

J           = 500
e2          = iws.random.skewed1d(J, Q, alpha=50)


s0          = iws.signal.sigmoid_pulse(Q=Q, q0=50, w=10, wfall=5, amp=1)
s1          = iws.signal.sigmoid_pulse(Q=Q, q0=50, w=50, wfall=5, amp=1)

s2          = iws.signal.sigmoid_pulse(Q=Q, q0=50, w=20, wfall=5, amp=1)
s3          = iws.signal.sigmoid_pulse(Q=Q, q0=50, w=20, wfall=5, amp=1.5)



### plot:
plt.close('all')
fig,AX = plt.subplots( 2, 2, figsize=(11,6) )
plt.get_current_fig_manager().window.move(0, 0)
ax0,ax1 = AX[0]
ax2,ax3 = AX[1]
### plot:
q   = np.linspace(0, 1, Q)
ax0.plot(q,  e0.T, 'k', lw=1 )
ax0.plot(q,  e1.T, 'b', lw=1 )
ax0.set_title('(a)  Error smoothness')

ax1.plot(q,  e2.T, 'k', lw=0.3 )
ax1.set_title('(b)  Error distribution (Gauss skewed)')

ax2.plot(q, s0, 'k')
ax2.plot(q, s1, 'b')
ax2.set_title('(c)  Signal width')

ax3.plot(q, s2, 'k')
ax3.plot(q, s3, 'b')
ax3.set_title('(d)  Signal amplitude')


plt.setp(AX, xlim=(0,1))
# plt.setp(AX[0], ylim=(-3.5,3.5))
plt.setp(AX[1], ylim=(-0.05,1.55))



# plt.setp(AX, xlim=(0,1), ylim=(-4,7))
plt.tight_layout()
plt.show()



dirREPO       = unipath.Path( os.path.dirname(__file__) ).parent.parent
fname_fig     = os.path.join( dirREPO, 'Figures', 'Simulation', 'fig_methods_general.pdf')
plt.savefig(fname_fig)