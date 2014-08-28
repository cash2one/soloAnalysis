from __future__ import division

def DC_offline(x):
	mean = sum(x)/len(x)
	return [i-mean for i in x]
	
def max_normalize(x):
	maxx = max(x)
	return [i/maxx for i in x]
	
def mean_normalize(x):
	if any(x):
		mean = sum(map(abs,x))/len(x)
		return [i/mean for i in x]
	else:
		return x
