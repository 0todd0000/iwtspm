

from math import sqrt,log
import numpy as np
from scipy import stats
from . import signal

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



def gauss( size=(1,) ):
	return np.random.randn(*size)
def gauss1d(J, Q):
	rcg = BernsteinSum(Q, rng=gauss)
	return rcg.rand(J)


def gauss1dnu(J, Q, FWHM):
	Q     = FWHM.size
	z     = np.random.randn(Q, J)
	s     = FWHM / (  (Q-1) * sqrt( 4*log(2) )  )
	dx    = 1. / (Q -1)
	x     = np.array([dx * np.arange(Q)])
	X     = np.repeat(x, Q, 0) 
	D     =  X - np.repeat(x.T, Q, 1)  #;   %distance matrix (relative to diagonal nodes)
	A     = np.exp(-0.5*D**2 /  (s**2) )
	
	[U,V]  =  np.linalg.eig(A.T)
	U,V    = np.real(U), np.real(V)
	U[U<eps] = 0
	U,V    = np.matrix(np.diag( np.sqrt(U) )), np.matrix(V)
	C      = V * U * V.T
	y      = (C * z).T
	return np.asarray(y)


def moyal( size=(1,) ):
	return stats.moyal.rvs( size=size ) - stats.moyal.expect()
def moyal1d(J, Q):
	rcg = BernsteinSum(Q, rng=moyal)
	return rcg.rand(J)
	

def skewed( alpha=0, size=(1,) ):
	return stats.skewnorm.rvs( alpha, size=size ) - stats.skewnorm.expect(np.mean, (alpha,)) 
def skewed1d(J, Q, alpha=0):
	def rng( size=(1,) ):
		return skewed(alpha=alpha, size=size)
	rcg = BernsteinSum(Q, rng=rng)
	return rcg.rand(J)



def generate_dataset(J, Q, sig_amp=1, sig_width=10, dist='gauss', distparams=None):
	if dist == 'gauss':
		rng = lambda: gauss1d( J , Q )
	elif dist == 'gaussnu':
		rng = lambda: gauss1dnu( J , Q , distparams[0] )
	elif dist == 'moyal':
		rng = lambda: moyal1d( J , Q )
	elif dist == 'skewed':
		rng = lambda: skewed1d( J , Q , alpha=distparams[0] )
	m0  = np.zeros( Q )
	m1  = signal.sigmoid_pulse(Q=Q, q0=50, w=sig_width, wfall=5, amp=sig_amp)
	y0  = m0 + rng()
	y1  = m1 + rng()
	return y0, y1
