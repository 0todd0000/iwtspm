
import os
import numpy as np
import iwtspm as iws



dir0     = os.path.join( iws.dirREPO, 'Data', 'Simulation' )
fnameNPZ = os.path.join( dir0, 'signalamp', '_results.npz')


with np.load(fnameNPZ) as Z:
	param_name   = str( Z['param_name'] )
	param_values = Z['param_values']
	proc         = Z['proc']
	p            = np.asarray(Z['p'], dtype=float) / 10000   # rescaled p values (p values saved as integers for smaller file sizes)


nproc      = 4      # unadjusted, IWT, SPM, SnPM
alpha      = 0.05

i            = param_values==0
p_unadjusted = p[ (proc==0) & i ]
p_iwt        = p[ (proc==1) & i ]
p_spm        = p[ (proc==2) & i ]
p_snpm       = iws.perf.snpm_correct_pvalues( p[ (proc==3) & i ] )

labels       = 'Unadjusted', 'IWT', 'SPM', 'SnPM'
for i,label in enumerate(labels):
	pp       = p[ (proc==i) & (param_values==0) ]
	if label=='SnPM':
		pp   = iws.perf.snpm_correct_pvalues( pp )
	fwer     = np.any(pp<alpha, axis=1).mean()
	print( f'FWER ({label}) = {fwer:05}')




# pp    = np.array([   for i in range(nproc)])
#
# b = (pp<alpha).mean(axis=1).mean(axis=1)