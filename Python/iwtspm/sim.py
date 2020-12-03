
import os, shutil
from . import prob


class Simulator(object):
	def __init__(self, wd, gen, suff=''):
		self.y0   = None
		self.y1   = None
		self.wd   = wd
		self.gen  = gen
		self.suff = suff

	def clear_wd(self):
		shutil.rmtree( self.wd )
		os.mkdir( self.wd )
		self.y0  = None
		self.y1  = None

	def get_data(self):
		return self.y0, self.y1
	
	def run_iteration(self):
		y0,y1    = self.gen()
		fdata    = os.path.join(self.wd, 'data%s.csv' %self.suff)
		fresults = os.path.join(self.wd, 'iwt%s.csv' %self.suff)
		p0       = prob.p_unadjusted(y0, y1)
		p1       = prob.p_iwt(y0, y1, niter=1000, fname_data=fdata, fname_results=fresults)
		p2       = prob.p_spm(y0, y1)
		p3       = prob.p_snpm(y0, y1, niter=1000)
		self.y0  = y0
		self.y1  = y1
		return p0,p1,p2,p3
