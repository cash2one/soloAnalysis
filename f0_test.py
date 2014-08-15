from tool.FFT import FFT
from tool.FFT import log
from wavGet import signal
import tool.normalizer as nml
import math
import matplotlib.pyplot as plt

def isLocalMax(x,ind):
	return (ind==0 or x[ind]>=x[ind-1]) and (ind==len(x)-1 or x[ind]>x[ind+1])

#auto-correlation function
def ACF(x,windowLength):
	n = log(x)
	x_FFT = FFT(x)
	y_FFT = FFT(x[windowLength-1::-1],n)
	mult = FFT([i*j for i,j in zip(x_FFT,y_FFT)][::-1])
	return [i.real/2**n for i in mult][windowLength-1:]

def f0_viaACF(x):
	if x[0]<0:
		x = [-i for i in x]
	ac,j = ACF(x,1000),1
	while ac[j]<0.6*ac[0] or not isLocalMax(ac,j):
		j += 1
	#plt.plot(x,'b')
	#plt.plot(nml.max_normalize(ac),'r')
	#plt.show()
	return 44100/j

print f0_viaACF(signal[2000:])
