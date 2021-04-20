
import iwtspm as iws



wd          = '/Users/todd/Desktop/Working/'
pname       = 'fwhm_ratio'
x           = [0.2, 0.25, 0.33, 0.5, 1, 2, 3, 4, 5]
niter       = 1000
seed        = 71



manager     = iws.sim.SimulationManager( wd )
manager.set_niter( niter )
manager.set_parameter( pname )
manager.set_parameter_values( x )
manager.run( seed0=seed )



