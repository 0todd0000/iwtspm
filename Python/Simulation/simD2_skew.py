
import os
import iwtspm as iws



wd          = os.path.join( os.path.dirname(__file__), 'wd' )
pname       = 'skew'
x           = list( range(-5,6) )
niter       = 10000
seed        = 82



manager     = iws.sim.SimulationManager( wd )
manager.set_niter( niter )
manager.set_parameter( pname )
manager.set_parameter_values( x )
manager.run( seed0=seed )



