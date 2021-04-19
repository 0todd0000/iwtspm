
import time
import os
import numpy as np
from matplotlib import pyplot as plt
import iwtspm as iws


wd          = '/Users/todd/Desktop/Working/'



# #(0) Run a single iteration:
# np.random.seed(0)
# ### initialize parameters:
# params       = iws.sim.SimulationParameters()
# params['nA'] = 5
# ### initialize simulator:
# sim          = iws.sim.Simulator(wd, params=params)
# sim.clear_wd()
# ### run tests:
# plt.close('all')
# p0,p1,p2,p3 = sim.run_iteration(plot=True)
# plt.show()


# #(1) Run multiple iterations:
# np.random.seed(0)
# ### initialize parameters:
# params          = iws.sim.SimulationParameters()
# params['nA']    = 5
# params['niter'] = 10
# ### initialize simulator:
# sim             = iws.sim.Simulator(wd, params=params)
# sim.clear_wd()
# sim.run_all_iterations(verbose=True)





# #(2) Run using script:
# path2script           = '/Users/todd/GitHub/iwtspm/Python/iwtspm/script_run_simulation.py'
# wd                    = '/Users/todd/Desktop/Working/'
# niter                 = 10
# param_name            = 'nA'
# param_value           = 3
# param_valuelist_index = 0
# seed                  = 0
# cmd                   = f'python {path2script} {wd} {niter} {param_name} {param_value} {param_valuelist_index} {seed}'
# os.system(cmd)
# # python /Users/todd/GitHub/iwtspm/Python/iwtspm/script_run_simulation.py /Users/todd/Desktop/Working/ nA 5 10 0 12345





#(3) Run using manager:
pname       = 'nA'
x           = list( range(4,37,2) )
manager     = iws.sim.SimulationManager(wd)
manager.set_niter(20)
manager.set_parameter('nA')
manager.set_parameter_values( [15, 20, 25] )  # save a _varvalues.npy dictionary
manager.run(seed0=0)



