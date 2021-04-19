
import sys,os
import numpy as np


# set path and import iwtspm
dirPARENT     = os.path.dirname( os.path.dirname( __file__ ) )
if dirPARENT not in sys.path:
	sys.path.insert( 0, dirPARENT )
import iwtspm as iws


def str2num(s):
	try:
		return int(s)
	except ValueError:
		return float(s)



if __name__ == '__main__':
	# parse command-line parameters
	values                = sys.argv[1:]
	wd                    = values[0]
	niter                 = int( values[1] )
	param_name            = values[2]
	param_value           = str2num( values[3] )
	param_valuelist_index = int( values[4] )
	seed                  = int( values[5] )
	# run iterations:
	np.random.seed( seed )
	params                = iws.sim.SimulationParameters()
	params[param_name]    = param_value
	params['niter']       = niter
	msg                   = f'{param_name}={param_value}'
	sim                   = iws.sim.Simulator(wd, params=params, suffix=param_valuelist_index)
	sim.run_all_iterations(verbose=True, msg=msg)






