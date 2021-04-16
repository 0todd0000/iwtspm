
import time
import os
import numpy as np
from matplotlib import pyplot as plt
import iwtspm as iws





# #(0) Run a single iteration:
# np.random.seed(0)
# dir0        = '/Users/todd/Desktop/Working/'
# ### initialize parameters:
# params      = iws.sim.SimulationParameters()
# params.set_nA(5)
# ### initialize simulator:
# sim         = iws.sim.Simulator(dir0, params=params)
# sim.clear_wd()
# ### run tests:
# plt.close('all')
# p0,p1,p2,p3 = sim.run_iteration(plot=True)
# plt.show()








#(1) Run multiple iterations:
# ----- START USER SPECIFICATIONS -----
### specify working directory base:
dir0        = '/Users/todd/Desktop/Working/'
### specify parameter values:
pname       = 'nA'
xx          = list( range(4,37,2) )
ind         = 0
# ----- END USER SPECIFICATIONS -----
x           = xx[ind]
np.random.seed( x )
params      = iws.sim.SimulationParameters()
params.set_nA( x )
params.niter = 10

sim         = iws.sim.Simulator(dir0, params, suffix=x)
sim.clear_wd()
sim.run_all()



# J0          = 36
# sfx         = f'-{suffix}-{J0}'
# fname_results = os.path.join(wd, f'results{sfx}.npy')











