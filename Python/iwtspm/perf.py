
'''
Performance metrics and convenience summary functions
'''

from math import floor
import numpy as np
from matplotlib import pyplot as plt
from . sim import SimulationParameters



def fpr(p, domain, alpha=0.05):
	pnd  = p[:, np.logical_not(domain)]
	b    = np.any( pnd<alpha , axis=1 )
	return b.mean()

def sensitivity(p, domain, alpha=0.05):
	pd   = p[:, domain]
	ds   = domain.sum()
	n    = ( pd<alpha ).sum( axis=1 )
	return (n / ds).mean()
	
# def fallout(p, domain, alpha=0.05):
# 	nd   = np.logical_not(domain)
# 	nds  = nd.sum()
# 	pnd  = p[:, nd]
# 	n    = ( pnd<alpha ).sum( axis=1 )
# 	return (n / nds).mean()

def performance(p, domain, alpha=0.05):
	m0   = fpr(p, domain, alpha=0.05)
	m1   = sensitivity(p, domain, alpha=0.05)
	# m2   = fallout(p, domain, alpha=0.05)
	return np.around( [m0, m1] , 5)


def get_domain(Q, width, sig_fallw=5):
	fw       = sig_fallw
	i0       = int( floor( 50 - (0.5 * width) - fw ) )
	i1       = i0 + width + 2*fw
	domain   = np.array( [False]*Q )
	domain[i0:i1+1] = True
	return domain



def plot_performance_results(fname_results, alpha=0.05, uxtransform=None):
	# load simulation results:
	with np.load(fname_results) as Z:
		param_name   = str( Z['param_name'] )
		param_values = Z['param_values']
		proc         = Z['proc']
		p            = np.asarray(Z['p'], dtype=float) / 10000
	# calculate performance: 
	Q          = p.shape[1]
	uproc      = np.unique(proc)
	x,ux       = param_values, np.unique( param_values )
	domain     = get_domain(Q, 40, sig_fallw=3)
	perf       = np.array([[performance( p[(proc==prc) & (x==u)] , domain, alpha)  for prc in uproc] for u in ux])
	# get baseline value:
	params     = SimulationParameters()
	blvalue    = params[param_name]
	# plot:
	fig,AX     = plt.subplots(1, 2, figsize=(8,3))
	ax0,ax1    = AX
	uxt        = ux if (uxtransform is None) else uxtransform(ux)
	blvaluet   = blvalue if (uxtransform is None) else uxtransform(blvalue)
	ax0.plot( uxt, perf[:,:,0] )
	ax1.plot( uxt, perf[:,:,1] )
	[ax.axvline( blvaluet, color='k', ls='--')  for ax in AX]
	# annotate:
	ax0.legend( ['Unadjusted', 'IWT', 'SPM', 'SnPM'] )
	[ax.set_ylim(-0.05, 1.05)  for ax in AX]
	[ax.set_xlabel('Parameter value') for ax in AX]
	ax0.set_ylabel('FPR')
	ax1.set_ylabel('Sensitivity')
	plt.tight_layout()

