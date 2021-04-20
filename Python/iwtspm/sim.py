
'''
Convenience classes for running simulations
'''


import os,shutil
import inspect,time
from subprocess import Popen
import numpy as np
from matplotlib import pyplot as plt
from . import prob as iwsprob
from . import rand as iwsrand
from . import signal as iwssignal




class SimulationParameters(dict):
	
	def __init__(self):
		d                     = {}
		# main parameters:
		d['Q']                = 101      # number of continuum points
		d['niter']            = 1000     # number of simulation iterations (datasets)
		# sample size parameters: 
		d['nA']               = 20       # sample size (Group A)
		d['nTotal']           = 40       # total sample size (GroupA + Group B)
		# signal parameters: 
		d['signal_amp']       = 1        # signal amplitude
		d['signal_center']    = 50       # signal center
		d['signal_fall']      = 5        # signal sigmoid falloff width
		d['signal_width']     = 40       # signal width
		d['mpwidth']          = None     # signal width (multipulse case)
		# smoothness parameters:
		d['fwhm']             = 20       # smoothness
		d['fwhm_ratio']       = 1        # smoothness ratio (D0:D1)
		# variance parameters:
		d['skew']             = None     # skewness parameter alpha
		d['sigmaA']           = 1        # standard deviation (Group A)
		d['sigmaB']           = 1        # standard deviation (Group B)
		d['sigma_ratio']      = 1        # standard deviation ratio (D0:D1)
		super().__init__( **d )
		self.__dict__         = self

	def __repr__(self):
		s  = 'SimulationParameters\n'
		n  = max( [len(key)  for key in self.keys()] )
		for key,value in self.items():
			k  = key.ljust(n)
			s +=  f'  {k} : {value}\n'
		return s

	def __getitem__(self, key):
		if key=='sample_size':
			return 20
		elif key=='nB':
			return self.nB
		elif key=='multipulse_width':
			return None
		else:
			return super().__getitem__(key)
	
	def __setitem__(self, key, value):
		if key=='sample_size':
			self['nA']     = value
			self['nTotal'] = 2 * value
		elif key=='multipulse_width':
			self['signal_amp']        = 0
			self['mpwidth']  = value
		else:
			super().__setitem__(key, value)

	@property
	def nB(self):
		return self['nTotal'] - self['nA']
		



class Simulator(object):
	def __init__(self, wd, params=None, suffix=None):
		self.gen     = None
		self.params  = SimulationParameters() if (params is None) else params
		self.simname = None
		self.suffix  = suffix
		self.wd      = wd
		# self._init_wd()
		self._init_gen()
		
	# def _init_wd(self):
	# 	caller       = inspect.stack()[2][0]
	# 	scriptpath   = inspect.getfile(caller)
	# 	_,sname      = os.path.split( scriptpath )
	# 	self.simname = sname.strip('.py').split('_')[1]
	# 	self.wd      = os.path.join( self._wdbase, self.simname)
	# 	if not os.path.exists( self.wd ):
	# 		os.mkdir( self.wd )
	
	def _init_gen(self):
		### assemble parameters:
		params       = self.params
		Q,q0         = params.Q, params.signal_center
		nA,nB        = params.nA, params.nB
		w,wf         = params.signal_width, params.signal_fall
		# sd,sdr       = params.sigmaB, params.sigma_ratio
		sdA,sdB,sdr  = params.sigmaA, params.sigmaB, params.sigma_ratio
		fwhm,fwhmr   = params.fwhm, params.fwhm_ratio
		sig_amp      = params.signal_amp
		sig_width    = params.signal_width
		### create variance and smoothness continua:
		sigma        = iwssignal.sigmoid_pulse_amps( Q=Q, q0=q0, w=w, wfall=wf, amp0=(sdB*sdr), amp1=sdB )
		fwhm         = iwssignal.sigmoid_pulse_amps( Q=Q, q0=q0, w=w, wfall=wf, amp0=(fwhm*fwhmr), amp1=fwhm)
		### assemble error distribution type and parameters:
		if params.skew is None:
			dist     = 'gauss_matern'
			dparams  = (sigma, fwhm)
		else:
			dist     = 'skewed'
			dparams  = (params.skew,)
		### create a random number generator:
		self.gen     = lambda: iwsrand.generate_dataset(Q, sample_sizes=(nA,nB), sigma=(sdA,sdB), sig_amp=sig_amp, sig_width=sig_width, dist=dist, distparams=dparams, multipulse_width=params.mpwidth)


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
	
	def run_iteration(self, plot=False, clean=False):
		y0,y1    = self.random()
		p0       = iwsprob.p_unadjusted(y0, y1)
		p1       = iwsprob.p_iwt(y0, y1, niter=1000, fname_data=self.filepath_data, fname_results=self.filepath_iwt)
		p2       = iwsprob.p_spm(y0, y1)
		p3       = iwsprob.p_snpm(y0, y1, niter=1000)
		if plot:
			self.plot_iteration(y0, y1, p0, p1, p2, p3)
		if clean:
			os.remove( self.filepath_data )
			os.remove( self.filepath_iwt )
		return p0,p1,p2,p3
		
	def run_all_iterations(self, verbose=True, msg=None):
		A           = []
		niter       = self.params.niter
		msg         = '' if (msg is None) else msg+'   '
		for i in range( niter ):
			t0          = time.time()
			if verbose:
				print( f'{msg}Iteration={i+1} of {niter}...')
			p0,p1,p2,p3 = self.run_iteration(plot=False, clean=True)
			if verbose:
				print(  '    Elapsed time: %.1f s\n' %(time.time() - t0) )
			A.append( np.hstack([ [0], 10000*p0]) )
			A.append( np.hstack([ [1], 10000*p1]) )
			A.append( np.hstack([ [2], 10000*p2]) )
			A.append( np.hstack([ [3], 10000*p3]) )
			np.save( self.filepath_results, np.asarray(A, dtype=np.uint16) )



class SimulationManager(object):
	def __init__(self, wdbase):
		self._wdbase       = wdbase
		self.niter         = 1000
		self.param_name    = None
		self.param_values  = None
		self.wd            = None
		self._init_wd()

	def _init_wd(self):
		caller       = inspect.stack()[2][0]
		scriptpath   = inspect.getfile(caller)
		_,sname      = os.path.split( scriptpath )
		self.simname = sname[:-3].split('_')[1]
		self.wd      = os.path.join( self._wdbase, self.simname)
		if not os.path.exists( self.wd ):
			os.mkdir( self.wd )

	def _assemble_results(self):
		A,X          = [],[]
		for i,x in enumerate(self.param_values):
			fnameNPY = os.path.join(self.wd, f'simt-{i}.npy')
			a        = np.load(fnameNPY)
			A.append(a)
			X       += [x] * a.shape[0]
		A,X          = np.vstack(A), np.array(X).flatten()
		procedure    = np.asarray(A[:,0], np.uint8)
		p            = A[:,1:]
		fnameRES     = os.path.join(self.wd, f'_results.npz')
		np.savez_compressed(fnameRES, proc=procedure, param_name=self.param_name, param_values=X, p=p)

	def set_niter(self, x):
		self.niter         = x
	def set_parameter(self, s):
		self.param_name    = s
	def set_parameter_values(self, x):
		self.param_values  = list( x )

	def run(self, seed0=0):
		path2script = os.path.join(  os.path.dirname( __file__ ) , 'script_run_simulation.py' )
		# # save parameter list values:
		# fnamePARAMS = os.path.join( self.wd, '_param_values.npz' )
		# np.savez(fnamePARAMS, name=self.param_name, values=self.param_values, niter=self.niter)
		# assemble commands:
		commands    = []
		for i,x in enumerate(self.param_values):
			seed    = seed0 + i
			cmd     = f'python {path2script} {self.wd} {self.niter} {self.param_name} {x} {i} {seed}'
			commands.append( cmd )
		# execute in parallel:
		procs       = [ Popen(c, shell=True) for c in commands ]
		for proc in procs:
			proc.wait()
		self._assemble_results()



