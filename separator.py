import numpy as np
import numpy.linalg as npl
from wavGet import get
from tool.FFT import *
import tool.denoiser as dn
import matplotlib.pyplot as plt
import tool.normalizer as nml

def sep(url):
	#print(len(signal))
	signal = get(url)
	#Constants
	N0 = (len(signal)-KAPPA)//ETA
	threshold = 6

	complex_spectrogram = np.array([STFT(signal,i) for i in range(0,N0)])
	spectrogram = np.vectorize(abs)((complex_spectrogram.T[:KAPPA//2+1]))
	'''np.array([[1,2],[3,4]],dtype=float)'''
	#print (n,m)
	
	A,S = NMF(spectrogram)

	return nml.max_normalize((A.T)[0])

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

'''#KL-divergence
def KLD(p,q):
	if abs(p)<1e-12:
		return q
	if abs(q)<1e-12:
		return p*math.log()
	return p*math.log(p/q)-p+q

#KL-distance between matrices
def D(A,B):
	sum = 0
	for i in range(len(A)):
		for j in range(len(A[i])):
			sum += KLD(A[i][j],B[i][i])
	return sum'''

def check(stg):
	for x in np.nditer(stg, op_flags = ['readwrite']):
		if x == 0:
			x[...] = 1e-9

#non-negative matrix factorization
def NMF(stg):
	
	check(stg)
	n,m = stg.shape
	r = 1#SVDF(stg,1)
	A = np.vectorize(abs)(np.random.randn(n,r))+np.ones((n,r))#np.array([[1],[2]])
	S = np.vectorize(abs)(np.random.randn(r,m))+np.ones((r,m))#np.array([[1,2]])
	lastD = 0
	
	while True:
		AS = np.dot(A,S)
		#print(AS)
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
	#stg = np.vectorize(lambda x:0+0j if abs(x)==0 else x/abs(x))(complex_spectrogram)*spec
	ans = [0]*(N0*ETA+KAPPA)
	#wave = map(lambda x:x.real,iFFT(spec))
	
	for i in range(0,N0):
		wave = map(lambda x:x.real,iFFT(spec))
		for j in range(0,KAPPA):
			c = coeff[i]
			if (i==0 and j<KAPPA//2) or (i==N0-1 and j>=KAPPA//2):
				c *= 1
			else:
				c *= Hann(KAPPA,j)
			ans[i*ETA+j] += wave[j]*c
	
	return ans

def recover_2(spec):
	ans = [0]*(N0*ETA+KAPPA)
	
	for i in range(0,N0):
		sp = (spec.T)[i]
		sp = np.concatenate((sp,sp[KAPPA//2-1:0:-1]), axis=0)
		wave = map(lambda x:x.real,iFFT(sp))
		for j in range(0,KAPPA):
			c = 1
			if (i==0 and j<KAPPA//2) or (i==N0-1 and j>=KAPPA//2):
				c *= 1
			else:
				c *= Hann(KAPPA,j)
			ans[i*ETA+j] += wave[j]*c
	
	return ans
	
def filter(wave):
	maxx = max(wave)
	return map(lambda x:0 if x<maxx*0.1 else x, wave)
