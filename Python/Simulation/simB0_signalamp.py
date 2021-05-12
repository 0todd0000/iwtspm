
import os
import iwtspm as iws



wd          = os.path.join( os.path.dirname(__file__), 'wd' )
pname       = 'signal_amp'
x           = [0, 0.5, 1, 1.5, 2.0, 2.5, 3]
niter       = 10000
seed        = 60



manager     = iws.sim.SimulationManager( wd )
manager.set_niter( niter )
manager.set_parameter( pname )
manager.set_parameter_values( x )
manager.run( seed0=seed )



