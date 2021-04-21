
import iwtspm as iws



wd          = '/Users/todd/Desktop/Working/'
pname       = 'sample_size'
x           = [5, 10, 15, 20, 25, 30, 40, 50, 80]
niter       = 10000
seed        = 50



manager     = iws.sim.SimulationManager( wd )
manager.set_niter( niter )
manager.set_parameter( pname )
manager.set_parameter_values( x )
manager.run( seed0=seed )



