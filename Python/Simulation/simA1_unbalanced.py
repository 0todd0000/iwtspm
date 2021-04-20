
import iwtspm as iws



wd          = '/Users/todd/Desktop/Working/'
pname       = 'nA'
x           = list( range(4,37,2) )
niter       = 1000
seed        = 51



manager     = iws.sim.SimulationManager( wd )
manager.set_niter( niter )
manager.set_parameter( pname )
manager.set_parameter_values( x )
manager.run( seed0=seed )



