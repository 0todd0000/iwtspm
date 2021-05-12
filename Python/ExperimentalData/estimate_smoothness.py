
'''
Estimate smoothness (FWHM) for all experimental datasets.
'''



import os
import numpy as np
import spm1d
import iwtspm as iws


def load_csv(fnameCSV):
	a             = np.loadtxt(fname_data, delimiter=',')
	group         = a[:,0]
	y             = a[:,1:]
	u             = np.unique(group)
	y0,y1         = y[group==u[0]], y[group==u[1]]
	return y0,y1

def estimate_fwhm(y0, y1):
	r0,r1         = y0 - y0.mean(axis=0), y1 - y1.mean(axis=0)
	r             = np.vstack( [r0, r1] )
	w             = spm1d.rft1d.geom.estimate_fwhm(r)
	return w


# Estimate FWHM for all datasets:
dirREPO           = iws.dirREPO
dataset_labels    = ['Kautz1991a', 'Kautz1991b', 'Neptune1999', 'Besier2009a', 'Besier2009b', 'Dorn2012']
w                 = []
for dataset_label in dataset_labels:
	fname_data    = os.path.join( dirREPO, 'Data', 'ExperimentalData', '%s.csv' %dataset_label)
	y0,y1         = load_csv(fname_data)
	ww            = estimate_fwhm( y0 , y1 )
	w.append( ww )


# Print results:
print('Estimated smoothness:')
print('---------------------')
for ss,ww in zip( dataset_labels , w ):
	print( '%-12s : %.1f' %(ss,ww) )
print('---------------------')
print( '%-12s : %.1f' %('Mean', np.mean(w) ) )

