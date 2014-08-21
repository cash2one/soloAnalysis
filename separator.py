import numpy as np
import numpy.linalg as npl
from wavGet import signal
from tool.FFT import *

#Constants
N0 = (len(signal)-KAPPA)//ETA
threshold = 6

spectrogram = np.array([STFT(signal,i) for i in range(0,N0)]).transpose()
n,m = spectrogram.shape

#matrix factorize via SVD
def SVDF(stg,outputType=0):
	U,s,V = npl.svd(spectrogram,full_matrices=False)
	
	i0 = 0
	while i0<len(s)-1 and s[i0]<=s[i0+1]*threshold:
		i0 += 1
	if outputType = 0:
		return (U,np.dot(s[:i0],V))
	else:
		return i0

def oneMat(i,j):
	return np.array([[1]*j]*i)

#KL-divergence
def KLD(p,q):
	return p*math.log(p/q)-p+q

#KL-distance between matrices	
def D(A,B):
	sum = 0
	for i in range(len(A)):
		for j in range(len(A[i])):
			sum += KLD(A[i][j],B[i][i])
	return sum

#non-negative matrix factorization, stg=A*S
def NMF(stg):
	
	r = SVDF(stg,1)
	A = np.vectorize(abs)(np.random.randn(n,r))
	S = np.vectorize(abs)(np.random.randn(r,m))
	lastD = 0
	
	while True:
		X = np.dot(A,S)
		if abs(D(stg,X)-lastD)<1e-10:
			break
		lastD = D(stg,X)
		A = A*np.dot(stg/X,S.transpose())/np.dot(oneMat(n,m),S.transpose())
		X = np.dot(A,S)
		S = S*np.dot(A.transpose(),stg/X)/np.dot(A.transpose(),oneMat(n,m))
	
	return A,S
