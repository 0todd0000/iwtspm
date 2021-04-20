
import iwtspm as iws



wd          = '/Users/todd/Desktop/Working/'
pname       = 'fwhm'
x           = [3, 10, 20, 30, 40, 50, 60]
niter       = 100
seed        = 70



manager     = iws.sim.SimulationManager( wd )
manager.set_niter( niter )
manager.set_parameter( pname )
manager.set_parameter_values( x )
manager.run( seed0=seed )



