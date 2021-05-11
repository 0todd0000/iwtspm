
'''
Calculation durations for the baseline scenario
'''

import os
import numpy as np
import time
import iwtspm as iws



# #(0) Run a single iteration:
# np.random.seed(0)
# wd        = os.path.join( os.path.dirname( __file__ ) , '_wd' )
# params    = iws.sim.SimulationParameters()  # baseline parameters
# sim       = iws.sim.Simulator(wd, params)
# y0,y1     = sim.random()
# # calculate p values:
# t0        = time.time();   p0 = iws.prob.p_unadjusted(y0, y1)
# t1        = time.time();   p1 = iws.prob.p_iwt(y0, y1, niter=1000, fname_data=sim.filepath_data, fname_results=sim.filepath_iwt)
# t2        = time.time();   p2 = iws.prob.p_spm(y0, y1)
# t3        = time.time();   p3 = iws.prob.p_snpm(y0, y1, niter=1000)
# t4        = time.time();   p4 = iws.perf.fdr_corrected_pvalues(p0)
# t5        = time.time()
# # calculate durations:
# durns     = [t1-t0, t2-t1, t3-t2, t4-t3, (t5-t4) + (t1-t0)]  # add d0 to the FDR calculation (FDR requires unadjusted p values)
# print( durns )





#(1) Run 1000 iterations:
np.random.seed(0)
wd        = os.path.join( os.path.dirname( __file__ ) , '_wd' )
params    = iws.sim.SimulationParameters()  # baseline parameters
sim       = iws.sim.Simulator(wd, params)
def report(d):
	if len(d)>1:
		m = np.mean( d , axis=0 )
		s = np.std( d, ddof=1, axis=0 )
		print( f'Iteration {len(d)}:')
		print( 'Averages: ', np.around(1000*m, 1) )
		print( 'SDs:      ', np.around(1000*s, 1) )
		print()
nsimiter  = 1000
durns     = []
for i in range(nsimiter):
	y0,y1 = sim.random()
	t0    = time.time();   p0 = iws.prob.p_unadjusted(y0, y1)
	t1    = time.time();   p1 = iws.prob.p_iwt(y0, y1, niter=1000, fname_data=sim.filepath_data, fname_results=sim.filepath_iwt)
	t2    = time.time();   p2 = iws.prob.p_spm(y0, y1)
	t3    = time.time();   p3 = iws.prob.p_snpm(y0, y1, niter=1000)
	t4    = time.time();   p4 = iws.perf.fdr_corrected_pvalues(p0)
	t5    = time.time()
	d     = [t1-t0, t2-t1, t3-t2, t4-t3, (t5-t4) + (t1-t0)]  # add d0 to the FDR calculation (FDR requires unadjusted p values)
	durns.append( d )
	report(durns)

