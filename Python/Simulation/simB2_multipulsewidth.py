
import iwtspm as iws



wd          = '/Users/todd/Desktop/Working/'
pname       = 'multipulse_width'
x           = [4, 8, 12, 16, 20]
niter       = 10000
seed        = 62



manager     = iws.sim.SimulationManager( wd )
manager.set_niter( niter )
manager.set_parameter( pname )
manager.set_parameter_values( x )
manager.run( seed0=seed )



