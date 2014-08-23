import numpy as np
import numpy.linalg as npl
from wavGet import signal
from tool.FFT import *
import matplotlib.pyplot as plt

#Constants
N0 = (len(signal)-KAPPA)//ETA
threshold = 6

complex_spectrogram = np.array([STFT(signal,i) for i in range(0,N0)])
spectrogram = np.vectorize(abs)((complex_spectrogram.T[:KAPPA//2+1]))
n,m = spectrogram.shape
print (n,m)

#matrix factorize via SVD
def SVDF(stg,outputType=0):
	U,s,V = npl.svd(spectrogram,full_matrices=False)
	
	i0 = 0
	while i0<len(s)-1 and s[i0]<=s[i0+1]*threshold:
		i0 += 1
	if outputType == 0:
		return (U,np.dot(s[:i0],V))
	else:
		return i0

#non-negative matrix factorization
def NMF(stg):
	
	r = SVDF(stg,1)
	A = np.vectorize(abs)(np.random.randn(n,r))#np.array([[1],[2]])
	S = np.vectorize(abs)(np.random.randn(r,m))#np.array([[1,2]])
	lastD = 0
	
	while True:
		AS = np.dot(A,S)
		stg_over_AS = stg/AS
		Dis = ((stg*np.log(stg_over_AS))-stg+AS).sum()
		if abs(Dis-lastD)<1e-4:
			break
		lastD = Dis
		
		A = A*np.dot(stg_over_AS,S.T)/S.sum(axis=1)
		AS = np.dot(A,S)
		stg_over_AS = stg/AS
		S = S*(np.dot(stg_over_AS.T,A)/A.sum(axis=0)).T
		print lastD
	
	return A,S

#Hanning window function
def Hann(N,k):
	return (1-math.cos(2*math.pi*k/(N-1)))/2

#len(spec) == KAPPA//2+1 == n, len(coeff) == N0 == m
def recover(spec,coeff):

	spec = np.concatenate((spec,spec[KAPPA//2-1:0:-1]), axis=0)
	print spec.shape
	stg = np.vectorize(lambda x:x/abs(x))(complex_spectrogram)*spec
	ans = [0]*(N0*ETA+KAPPA)
	
	for i in range(0,N0):
		wave = map(lambda x:x.real,iFFT(stg[i]))
		for j in range(0,KAPPA):
			c = coeff[i]
			if i==0 and j<KAPPA//2 or i==N0-1 and j>=KAPPA//2:
				c *= 1
			else:
				c *= Hann(KAPPA,j)
			ans[i*ETA+j] += wave[j]*c
	
	return ans
