
'''
Convenience module for generating simple sigmoid pulse signals
'''


import numpy as np


def multi_pulse(Q=101, q=[50], w=10, wfall=5):
	a           = np.zeros(Q)
	for qq in q:
		b       = sigmoid_pulse(Q, qq, w, wfall, 1)
		a      += b
	return a


def sigmoid_step(Q=101, q0=50, q1=75, x0=0, x1=1):
	z          = np.zeros(Q)
	zz         = 6
	z[:q0]     = -zz
	z[q1:]     = +zz
	z[q0:q1]   = np.linspace(-zz, zz, q1-q0)
	y          = 1.0 / (1.0 + np.exp(-1.0 * z))
	y          = (y - y[0]) / (y[-1]-y[0])
	y          = x0 + (y * (x1-x0))
	return y


def sigmoid_pulse(Q=101, q0=50, w=10, wfall=5, amp=1):
	c          = q0              # pulse center
	w2         = int( w / 2) # half width
	q01        = c - w2 + 1
	q00        = q01 - wfall
	q10        = c + w2
	q11        = q10 + wfall
	y0         = sigmoid_step(Q, q0=q00, q1=q01, x0=0, x1=amp)
	y1         = sigmoid_step(Q, q0=q10, q1=q11, x0=amp, x1=0)
	return y0 + y1 - amp
	

def sigmoid_pulse_amps(Q=101, q0=50, w=10, wfall=5, amp0=0, amp1=1):
	y = sigmoid_pulse(Q, q0, w, wfall, 1)
	return y * (amp1 - amp0) + amp0
