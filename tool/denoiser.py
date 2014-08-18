from __future__ import division
from FFT import convolution
import math

#turn an arbitrary list into a PDF
def PDFturner(x):
	s = sum(x)
	return [i/s for i in x]

def plane(n):
	return [1/n]*n

def triangle(n):
	return PDFturner(range(1,n//2+1)+range((n+1)//2,0,-1))

def Guassian(n,SIGMA):
	#Here sd is SIGMA*n
	return PDFturner([math.exp(-(i-(n-1)/2)**2/(2*SIGMA**2*n**2)) for i in range(0,n)])

#Gaussian Filter
def GFilter(x,k):
	return [i.real for i in convolution(x,Guassian(k,0.25))]
