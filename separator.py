import numpy as np
import numpy.linalg as npl
from wavGet import signal
from tool.FFT import *

#Constants
N0 = (len(signal)-KAPPA)//ETA
threshold = 6

spectrogram = np.array([STFT(signal,i) for i in range(0,N0)]).T
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
	A = np.vectorize(abs)(np.random.randn(n,r))
	S = np.vectorize(abs)(np.random.randn(r,m))
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
