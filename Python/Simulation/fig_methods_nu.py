
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
J,Q         = 20, 101
sig_amp     = 3
sig_width   = 30
# Case 1:
fwhm        = iws.signal.sigmoid_pulse_amps(Q=101, q0=50, w=30, wfall=15, amp0=10, amp1=30)
m0          = np.zeros( Q )
m1          = iws.signal.sigmoid_pulse(Q=Q, q0=50, w=sig_width, wfall=10, amp=sig_amp)
e0          = iws.random.gauss1dnu( J , Q , fwhm )
e1          = iws.random.gauss1dnu( J , Q , fwhm )
y0          = m0 + e0
y1          = m1 + e1
# Case 2:
fwhmB       = iws.signal.sigmoid_pulse_amps(Q=101, q0=50, w=30, wfall=15, amp0=30, amp1=10)
m0B         = np.zeros( Q )
m1B         = iws.signal.sigmoid_pulse(Q=Q, q0=50, w=sig_width, wfall=10, amp=sig_amp)
e0B         = iws.random.gauss1dnu( J , Q , fwhmB )
e1B         = iws.random.gauss1dnu( J , Q , fwhmB )
y0B         = m0B + e0B
y1B         = m1B + e1B



#(1) Plot:
plt.close('all')
fig,AX = plt.subplots( 2, 3, figsize=(11,6) )
plt.get_current_fig_manager().window.move(0, 0)
ax0,ax1,ax2 = AX[0]
ax3,ax4,ax5 = AX[1]
### plot:
q   = np.linspace(0, 1, Q)
ax0.plot(q,  e0.T, 'k', lw=0.3 )
ax0.plot(q,  e1.T, 'k', lw=0.3 )
ax0.axvspan(0.3, 0.7, alpha=0.5, color='0.7')
[ax0.text(x, 0.8, s, ha='center', transform=ax0.transAxes)  for x,s in zip([0.15, 0.5, 0.85], ['Rough', 'Smooth', 'Rough'] )]

ax1.plot(q,  m0, 'k', lw=5, label='A' )
ax1.plot(q,  m1, 'r', lw=2, label='B' )
ax1.legend(loc='lower left', bbox_to_anchor=(0.8,0.9))
ax1.axvspan(0.3, 0.7, alpha=0.5, color='0.7')
[ax1.text(x, 0.8, s, ha='center', transform=ax1.transAxes)  for x,s in zip([0.15, 0.5, 0.85], ['No Signal', 'Signal', 'No Signal'] )]

h0 = ax2.plot(q,  y0.T, 'k', lw=0.3)[0]
h1 = ax2.plot(q,  y1.T, 'r', lw=0.3)[0]
ax2.legend([h0,h1], ['A','B'])


ax3.plot(q,  e0B.T, 'k', lw=0.3 )
ax3.plot(q,  e1B.T, 'k', lw=0.3 )
ax3.axvspan(0.3, 0.7, alpha=0.5, color='0.7')
[ax3.text(x, 0.8, s, ha='center', transform=ax3.transAxes)  for x,s in zip([0.15, 0.5, 0.85], ['Smooth', 'Rough', 'Smooth'] )]

ax4.plot(q,  m0B, 'k', lw=5, label='A' )
ax4.plot(q,  m1B, 'r', lw=2, label='B' )
ax4.axvspan(0.3, 0.7, alpha=0.5, color='0.7')


h0 = ax5.plot(q,  y0B.T, 'k', lw=0.3)[0]
h1 = ax5.plot(q,  y1B.T, 'r', lw=0.3)[0]






titles = ['Error', 'Signal', 'Dataset  (Error + Signal)']
[ax.set_title(s)  for ax,s in zip(AX[0],titles)]
ax0.set_ylabel('Case 1', size=18)
ax3.set_ylabel('Case 2', size=18)

plt.setp(AX, xlim=(0,1), ylim=(-4,7))
plt.tight_layout()
plt.show()



# dirREPO       = unipath.Path( os.path.dirname(__file__) ).parent.parent
# fname_fig     = os.path.join( dirREPO, 'Figures', 'Simulation', 'fig_methods_nu.pdf')
# plt.savefig(fname_fig)