
'''
Performance metrics and convenience summary functions
'''

from math import floor
import numpy as np
from statsmodels.stats.multitest import fdrcorrection
from matplotlib import pyplot as plt
from . sim import SimulationParameters
from . import signal as iwssignal



def fdr_corrected_pvalues(p, alpha=0.05):
	pfdr = fdrcorrection(p, alpha=alpha, method='indep', is_sorted=False)[1]
	return pfdr

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


def get_multipulse_domain(Q=101, q=[20,50,80], w=20):
	a = iwssignal.multi_pulse(Q=Q, q=q, w=w)
	return np.asarray(a, dtype=bool)


def load_sim_results(fname_results, alpha=0.05):
	# define an FDR correction function:
	fdrc = lambda p: np.array([fdr_corrected_pvalues(pp, alpha=alpha)  for pp in p])
	# load simulation results:
	with np.load(fname_results) as Z:
		param_name   = str( Z['param_name'] )
		param_values = Z['param_values']
		proc         = Z['proc']
		p            = np.asarray(Z['p'], dtype=float) / 10000   # rescaled p values (p values saved as integers for smaller file sizes)
	# calculate performance:
	Q           = p.shape[1]
	uproc       = np.unique(proc)
	x,ux        = param_values, np.unique( param_values )
	if param_name == 'signal_width':
		domains = [get_domain(Q, x, sig_fallw=5)  for x in ux]
		perf    = np.array([[performance( p[(proc==prc) & (x==u)] , d, alpha)  for prc in uproc] for u,d in zip(ux,domains)])
		perffdr = np.array([performance(   fdrc(  p[(proc==0) & (x==u)]  ), d, alpha)    for u,d in zip(ux,domains)])
	elif param_name == 'multipulse_width':
		domains = [get_multipulse_domain(Q=101, q=[20,50,80], w=x)  for x in ux]
		perf    = np.array([[performance( p[(proc==prc) & (x==u)] , d, alpha)  for prc in uproc] for u,d in zip(ux,domains)])
		perffdr = np.array([performance(   fdrc(  p[(proc==0) & (x==u)]  ), d, alpha)    for u,d in zip(ux,domains)])
	else:
		domain  = get_domain(Q, 40, sig_fallw=5)
		perf    = np.array([[performance( p[(proc==prc) & (x==u)] , domain, alpha)  for prc in uproc] for u in ux])
		perffdr = np.array([performance(   fdrc(  p[(proc==0) & (x==u)]  ), domain, alpha)    for u in ux])
	# get baseline value:
	blvalue     = SimulationParameters()[param_name]
	return ux,perf,perffdr,blvalue



def plot_performance_results(fname_results, alpha=0.05, uxtransform=None):
	# # load simulation results:
	# with np.load(fname_results) as Z:
	# 	param_name   = str( Z['param_name'] )
	# 	param_values = Z['param_values']
	# 	proc         = Z['proc']
	# 	p            = np.asarray(Z['p'], dtype=float) / 10000
	# # calculate performance:
	# Q           = p.shape[1]
	# uproc       = np.unique(proc)
	# x,ux        = param_values, np.unique( param_values )
	# if param_name == 'signal_width':
	# 	domains = [get_domain(Q, x, sig_fallw=5)  for x in ux]
	# 	perf    = np.array([[performance( p[(proc==prc) & (x==u)] , d, alpha)  for prc in uproc] for u,d in zip(ux,domains)])
	# elif param_name == 'multipulse_width':
	# 	domains = [get_multipulse_domain(Q=101, q=[20,50,80], w=x)  for x in ux]
	# 	perf    = np.array([[performance( p[(proc==prc) & (x==u)] , d, alpha)  for prc in uproc] for u,d in zip(ux,domains)])
	# else:
	# 	domain  = get_domain(Q, 40, sig_fallw=5)
	# 	perf    = np.array([[performance( p[(proc==prc) & (x==u)] , domain, alpha)  for prc in uproc] for u in ux])
	# # get baseline value:
	# params      = SimulationParameters()
	# blvalue     = params[param_name]
	ux,perf,blvalue = load_sim_results(fname_results, alpha=alpha)
	# plot:
	fig,AX      = plt.subplots(1, 2, figsize=(8,3))
	ax0,ax1     = AX
	uxt         = ux if (uxtransform is None) else uxtransform(ux)
	ax0.plot( uxt, perf[:,:,0] )
	ax1.plot( uxt, perf[:,:,1] )
	if blvalue is not None:
		blvaluet = blvalue if (uxtransform is None) else uxtransform(blvalue)
		[ax.axvline( blvaluet, color='k', ls='--')  for ax in AX]
	# annotate:
	ax0.legend( ['Unadjusted', 'IWT', 'SPM', 'SnPM'] )
	[ax.set_ylim(-0.05, 1.05)  for ax in AX]
	[ax.set_xlabel('Parameter value') for ax in AX]
	ax0.set_ylabel('FPR')
	ax1.set_ylabel('Sensitivity')
	plt.tight_layout()


