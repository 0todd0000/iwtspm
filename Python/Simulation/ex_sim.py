
'''
Example single simulation iteration using baseline parameters (see manuscript).

Baseline parameters:

### Sample parameters:
- sample size = 20
- signal amplitude = 1.5
- signal width = 0.4

### Error parameters:
- error distribution = Gaussian 
- SD = 1
- SD ratio = 1.0  (same standard deviation everywhere)
- FWHM (smoothness) = 0.2
- FWHM ratio = 1.0 (same smoothness everywhere)
'''

import os
import numpy as np
from matplotlib import pyplot as plt
import iwtspm as iws





#(0) Run a single iteration:
np.random.seed(0)
wd          = os.path.join( os.path.dirname( __file__ ) , '_wd' )
### set baseline parameters:
Q           = 101   # domain size
J           = 20    # sample size
sig_amp     = 1     # signal amplitude
sig_width   = 40    # signal width (100ths)
sd          = 1     # standard deviation
sd_ratio    = 1     # standard deviation ratio (D0:D1)
fwhm        = 20
fwhm_ratio  = 1
### construct simulation objects:
s           = iws.signal.sigmoid_pulse_amps( Q=Q, q0=50, w=sig_width, wfall=5, amp0=(sd*sd_ratio), amp1=sd )
w           = iws.signal.sigmoid_pulse_amps( Q=Q, q0=50, w=sig_width, wfall=5, amp0=(fwhm*fwhm_ratio), amp1=fwhm)
gen         = lambda: iws.random.generate_dataset(J, Q, sig_amp=sig_amp, sig_width=sig_width, dist='gauss_matern', distparams=(s,w))
# y0,y1       = gen()
sim         = iws.sim.Simulator(wd, gen, suff='')
sim.clear_wd()
p0,p1,p2,p3 = sim.run_iteration()
y0,y1       = sim.get_data()
### plot:
plt.close('all')
fig,AX = plt.subplots( 1, 2, figsize=(8,3) )
plt.get_current_fig_manager().window.move(0, 0)
ax0,ax1 = AX.flatten()
### plot dataset:
q   = np.linspace(0, 1, Q)
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
plt.tight_layout()
plt.show()







