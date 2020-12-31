
'''
Convenience module for generating smooth, random 1D data
'''

from math import sqrt,log,pi
import numpy as np
from scipy import stats
from scipy.special import gamma
from scipy.special import kv as besselk
from . import signal
from spm1d import rft1d

eps         = np.finfo(np.float).eps



class BernsteinSum(object):
	def __init__(self, Q, q=None, sigma=None, rng=np.random.randn):
		self.Q      = int(Q)
		self.q      = np.linspace(0, 1, self.Q) if (q is None) else q
		self.sigma  = np.ones(self.Q) if (sigma is None) else sigma
		self.rng    = rng
		# calculate basis functions:
		q           = self.q
		self.f      = np.array([ (1-q)**6,   6*q*(1-q)**5  , 15*q**2*(1-q)**4  ,  20*q**3*(1-q)**3  ,  15*q**4*(1-q)**2  ,  6*q**5*(1-q)  ,  q**6 ])
		self.nbasis = self.f.shape[0]
		self.fnorm  = self.f / np.linalg.norm(self.f, axis=0)

	def rand(self, J=1):
		return (self.fnorm.T @ np.squeeze(self.rng( size=(self.nbasis, J) ))).T * self.sigma.T



def gauss1dns(J, Q, fwhm=10, s=1):
	'''
	Nonstationary, smooth Gaussian 1D noise
	'''
	e     = rft1d.randn1d(J, Q, FWHM=fwhm, pad=True)
	return s * e

def skewed( alpha=0, size=(1,) ):
	return stats.skewnorm.rvs( alpha, size=size ) - stats.skewnorm.expect(np.mean, (alpha,)) 
def skewed1d(J, Q, alpha=0):
	'''
	Skewed, smooth Gaussian 1D noise
	'''
	def rng( size=(1,) ):
		return skewed(alpha=alpha, size=size)
	rcg = BernsteinSum(Q, rng=rng)
	return rcg.rand(J)


def rho2fwhm(x):
	return 92.98198 * x + 0.34888
def fwhm2rho(x):
	return 0.010751 * x -0.00365

def matern(d, rho, nu, phi=1):
	'''
	Modified from matern.m in the BFDA package for Matlab (Yang & Ren, 206)
	
	Downloaded 2020-12-11
	
	Yang J, Ren P (2019). BFDA: A matlab toolbox for bayesian functional data analysis. J Stat Soft 89(2): doi: 10.18637/jss.v089.i02
	10.18637/jss.v089.i02
	https://www.jstatsoft.org/article/view/v089i02
	'''
	dm        = (d * sqrt(2*nu)) / rho
	dm[dm==0] = 1e-10
	con       = 1 / (  2**(nu-1) * gamma(nu) )
	cov       = phi * con * (dm**nu) * besselk(nu, dm)
	return cov


def cholesky(sig):
	'''
	Modified from mychol.m in the BFDA package for Matlab (Yang & Ren, 206)
	
	Downloaded 2020-12-11
	
	Yang J, Ren P (2019). BFDA: A matlab toolbox for bayesian functional data analysis. J Stat Soft 89(2): doi: 10.18637/jss.v089.i02
	10.18637/jss.v089.i02
	https://www.jstatsoft.org/article/view/v089i02
	'''
	U,S,V = np.linalg.svd(sig)
	DS    = S
	DS    = np.sqrt(DS)
	minDS = np.mean(DS)*10e-8
	DS[DS < 0] = minDS
	L = U @ np.diag(DS)
	return L
	
def randn1d_matern(n, p, s=1, fwhm=10, order=5):
	'''
	Modified from sim_gfd.m in the BFDA package for Matlab (Yang & Ren, 206)
	
	Downloaded 2020-12-11
	
	Yang J, Ren P (2019). BFDA: A matlab toolbox for bayesian functional data analysis. J Stat Soft 89(2): doi: 10.18637/jss.v089.i02
	10.18637/jss.v089.i02
	https://www.jstatsoft.org/article/view/v089i02
	'''
	J          = np.ones( (p, 1) )
	pgrid      = np.arange(0.001, pi/2+0.01, (pi/2)/(p-1))
	pgridm     = np.array( [pgrid] )
	D          = np.abs( J @ pgridm - pgridm.T @ J.T )
	rho        = fwhm2rho( fwhm )
	cov        = matern(D, rho, order)
	L          = cholesky( cov )
	r          = ( L @ np.random.randn(p, n) ).T
	r          = r * s
	return r

	

def generate_dataset(J, Q, sig_amp=1, sig_width=10, dist='gauss', distparams=None):
	if dist == 'gauss_matern':
		rng = lambda: randn1d_matern( J , Q , s=distparams[0] , fwhm=distparams[1] )
	elif dist == 'gaussns':
		rng = lambda: gauss1dns( J , Q , *distparams )
	elif dist == 'skewed':
		rng = lambda: skewed1d( J , Q , alpha=distparams[0] )
	m0  = np.zeros( Q )
	m1  = signal.sigmoid_pulse(Q=Q, q0=50, w=sig_width, wfall=5, amp=sig_amp)
	y0  = m0 + rng()
	y1  = m1 + rng()
	return y0, y1
