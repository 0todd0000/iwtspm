
'''
Example single simulation iteration using baseline parameters.

Find baseline parameters descriptions in the manuscript (Table 2)
'''

import os
import numpy as np
from matplotlib import pyplot as plt
import iwtspm as iws





#(0) Run a single iteration:
np.random.seed(0)
wd          = os.path.join( os.path.dirname( __file__ ) , '_wd' )
params      = iws.sim.SimulationParameters()   # baseline parameters
sim         = iws.sim.Simulator(wd, params, suffix='')
sim.clear_wd()
p0,p1,p2,p3 = sim.run_iteration()
y0,y1       = sim.get_data()
### plot:
plt.close('all')
fig,AX = plt.subplots( 1, 2, figsize=(8,3) )
plt.get_current_fig_manager().window.move(0, 0)
ax0,ax1 = AX.flatten()
### plot dataset:
q   = np.linspace(0, 1, params.Q)
ax0.plot(q,  y0.T, 'k', lw=0.5 )
ax0.plot(q,  y1.T, 'r', lw=0.5 )
### plot p curves
ax1.plot(q, p0, '0.7', lw=3, label='Unadjusted')
ax1.plot(q, p1, 'b', label='IWT')
ax1.plot(q, p2, 'c', label='SPM')
ax1.plot(q, p3, 'm', label='SnPM')
ax1.axhline(0.05, color='r', linestyle='--')
plt.sca(ax1)
plt.legend()
plt.tight_layout()
plt.show()







