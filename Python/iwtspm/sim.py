
'''
Convenience class for running simulations

(this saves only about 10 lines of code in simulation scripts)
'''


import os,shutil
import inspect,time
import pprint
import numpy as np
from matplotlib import pyplot as plt
from . import prob as iwsprob
from . import random as iwsrandom
from . import signal as iwssignal



class SimulationParameters(object):
	
	def __init__(self):
		self.Q             = 101      # number of continuum points
		self.nA            = 20       # sample size (Group A)
		self.nB            = 20       # sample size (Group B)
		self.niter         = 1000     # number of simulation iterations (datasets)
		self.sigmaA        = 1        # standard deviation (Group A)
		self.sigmaB        = 1        # standard deviation (Group B)
		self.sigma_ratio   = 1        # standard deviation ration (inside:outside signal region)
		self.error_type    = 'Gauss'  # error model
		self.signal_amp    = 1        # signal amplitude
		self.signal_center = 50       # signal center
		self.signal_fall   = 5        # signal sigmoid falloff width
		self.signal_width  = 40       # signal width
		self.fwhm          = 20       # smoothness
		self.fwhm_ratio    = 1        # smoothness ration (inside:outside signal region)

	def __repr__(self):
		s  = 'SimulationParameters\n'
		s += pprint.pformat( vars(self), indent=4)
		return s

	@property
	def ntotal(self):
		return self.nA + self.nB
		
	def set_nA(self, x):
		n = self.ntotal
		self.nA   = x
		self.nB   = n - x



class Simulator(object):
	def __init__(self, wdbase, params=None, suffix=None):
		self._wdbase = wdbase
		self.gen     = None
		self.params  = SimulationParameters() if (params is None) else params
		self.simname = None
		self.suffix  = suffix
		self.wd      = None
		self._init_wd()
		self._init_gen()
		
	def _init_wd(self):
		caller       = inspect.stack()[2][0]
		scriptpath   = inspect.getfile(caller)
		_,sname      = os.path.split( scriptpath )
		self.simname = sname.strip('.py').split('_')[1]
		self.wd      = os.path.join( self._wdbase, self.simname)
		if not os.path.exists( self.wd ):
			os.mkdir( self.wd )
	
	def _init_gen(self):
		### assemble parameters:
		params       = self.params
		Q,q0         = params.Q, params.signal_center
		nA,nB        = params.nA, params.nB
		w,wf         = params.signal_width, params.signal_fall
		sd,sdr       = params.sigmaB, params.sigma_ratio
		fwhm,fwhmr   = params.fwhm, params.fwhm_ratio
		sig_amp      = params.signal_amp
		sig_width    = params.signal_width
		### create variance and smoothness continua:
		sigma        = iwssignal.sigmoid_pulse_amps( Q=Q, q0=q0, w=w, wfall=wf, amp0=(sd*sdr), amp1=sd )
		fwhm         = iwssignal.sigmoid_pulse_amps( Q=Q, q0=q0, w=w, wfall=wf, amp0=(fwhm*fwhmr), amp1=fwhm)
		### create a random number generator:
		self.gen     = lambda: iwsrandom.generate_dataset(Q, sample_sizes=(nA,nB), sigma=(sd,sd), sig_amp=sig_amp, sig_width=sig_width, dist='gauss_matern', distparams=(sigma,fwhm))


	@property
	def filepath_data(self):
		fname   = 'data.csv' if (self.suffix is None) else f'data-{self.suffix}.csv'
		return os.path.join(self.wd, fname)
	@property
	def filepath_iwt(self):
		fname   = 'iwt.csv' if (self.suffix is None) else f'iwt-{self.suffix}.csv'
		return os.path.join(self.wd, fname)
	@property
	def filepath_results(self):
		fname   = 'simt.npy' if (self.suffix is None) else f'simt-{self.suffix}.npy'
		return os.path.join(self.wd, fname)

	def clear_wd(self):
		shutil.rmtree( self.wd )
		os.mkdir( self.wd )
		self.y0     = None
		self.y1     = None


	def plot_iteration(self, y0, y1, p0, p1, p2, p3):
		fig,AX  = plt.subplots( 1, 2, figsize=(8,3), constrained_layout=True )
		ax0,ax1 = AX.flatten()
		### plot dataset:
		q   = np.linspace(0, 1, self.params.Q)
		ax0.plot(q,  y0.T, 'k', lw=0.5 )
		ax0.plot(q,  y1.T, 'r', lw=0.5 )
		### plot p curves
		ax1.plot(q, p0, '0.7', lw=3, label='Unadjusted')
		ax1.plot(q, p1, 'b', label='IWT')
		ax1.plot(q, p2, 'c', label='SPM')
		ax1.plot(q, p3, 'm', label='SnPM')
		ax1.axhline(0.05, color='r', linestyle='--')
		plt.sca(ax1)
		plt.legend()


	def random(self):
		y0,y1 = self.gen()
		return y0,y1
	
	def run_iteration(self, plot=False):
		y0,y1    = self.random()
		p0       = iwsprob.p_unadjusted(y0, y1)
		p1       = iwsprob.p_iwt(y0, y1, niter=1000, fname_data=self.filepath_data, fname_results=self.filepath_iwt)
		p2       = iwsprob.p_spm(y0, y1)
		p3       = iwsprob.p_snpm(y0, y1, niter=1000)
		if plot:
			self.plot_iteration(y0, y1, p0, p1, p2, p3)
		return p0,p1,p2,p3
		
	def run_all(self, verbose=True):
		A           = []
		x           = -1 if (self.suffix is None) else self.suffix
		niter       = self.params.niter
		for i in range( niter ):
			t0          = time.time()
			if verbose:
				print( f'x={x}, iter={i+1} of {niter}...')
			p0,p1,p2,p3 = self.run_iteration(plot=False)
			if verbose:
				print( f'Elapsed time: {time.time() - t0}\n' )
			A.append( np.hstack([ [0, x], p0]) )
			A.append( np.hstack([ [1, x], p1]) )
			A.append( np.hstack([ [2, x], p2]) )
			A.append( np.hstack([ [3, x], p3]) )
			np.save( self.filepath_results, A )
			
		
		

def myfn(x):
	caller = inspect.stack()[1][0]
	print( inspect.getfile(caller) )
	return x + 1
	
	




# class Simulator(object):
# 	def __init__(self, wd, gen, suff=''):
# 		self.y0   = None
# 		self.y1   = None
# 		self.wd   = wd
# 		self.gen  = gen
# 		self.suff = suff
#
# 	def clear_wd(self):
# 		shutil.rmtree( self.wd )
# 		os.mkdir( self.wd )
# 		self.y0  = None
# 		self.y1  = None
#
# 	def get_data(self):
# 		return self.y0, self.y1
#
# 	def run_iteration(self):
# 		y0,y1    = self.gen()
# 		fdata    = os.path.join(self.wd, 'data%s.csv' %self.suff)
# 		fresults = os.path.join(self.wd, 'iwt%s.csv' %self.suff)
# 		p0       = prob.p_unadjusted(y0, y1)
# 		p1       = prob.p_iwt(y0, y1, niter=1000, fname_data=fdata, fname_results=fresults)
# 		p2       = prob.p_spm(y0, y1)
# 		p3       = prob.p_snpm(y0, y1, niter=1000)
# 		self.y0  = y0
# 		self.y1  = y1
# 		return p0,p1,p2,p3

	# def run_iteration(self, J0=None, sd0=None):
	# 	y0,y1    = self.gen()
	# 	if J0 is not None:
	# 		y       = np.vstack([y0, y1])
	# 		y0,y1   = y[:J0], y[J0:]
	# 	elif sd0 is not None:
	# 		y0      = sd0 * y0
	# 	fdata    = os.path.join(self.wd, 'data%s.csv' %self.suff)
	# 	fresults = os.path.join(self.wd, 'iwt%s.csv' %self.suff)
	# 	p0       = prob.p_unadjusted(y0, y1)
	# 	p1       = prob.p_iwt(y0, y1, niter=1000, fname_data=fdata, fname_results=fresults)
	# 	p2       = prob.p_spm(y0, y1)
	# 	p3       = prob.p_snpm(y0, y1, niter=1000)
	# 	self.y0  = y0
	# 	self.y1  = y1
	# 	return p0,p1,p2,p3


# baseline_parameters = {
# 	'Q'            : 101,
# 	'sample_sizes' : (20, 20),
# 	'sigmas'       : (1, 1),
# 	'error_type'   : 'Gauss',
# 	'signal_amp'   : 1,
# 	'signal_width' : 40,
# 	'sigms_ratio'  : 1,
# 	'fwhm'         : 20,
# 	'fwhm_ratio'   : 1,
# 	}






# def get_simname_from_scriptname( scriptpath ):
# 	_,sname     = os.path.split( scriptpath )
# 	simname     = sname.strip('.py').split('_')[1]
# 	return simname