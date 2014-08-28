from __future__ import division
from wavGet import get
import tool.denoiser as dn
import matplotlib.pyplot as plt

def linearpy(p1x,p1y,p2x,p2y,px):
	return (p2y*(px-p1x)-p1y*(px-p2x))/(p2x-p1x)

def env(url):
	
	signal = get(url)
	#plt.plot(signal,'b')
	#constant
	num = 100
	
	l = len(signal)
	while signal[l-1]<1e-6:
		l = l-1
	signal = map(abs,signal[:l])
	while signal[0]<1e-6:
		signal = signal[1:]
	
	signal = dn.GFilter(signal,1000)
	#maxx = max(signal)
	#start = signal.index(maxx)
	
	signal = [signal[int(i/num*l)] for i in range(0,num)]
	#plt.plot(signal,'r')
	#plt.show()
	return signal


#env(raw_input())
'''maxip = [(0,maxx)]
for i in range(1,num):
	if i == num-1 or (signal[i]>signal[i-1] and signal[i]>signal[i+1]):
		maxip += [(i,signal[i])]
		maxx = signal[i]
maxip = [(l-1,signal[l-1])]
for i in range(l-2,start-1,-1):
	if signal[i]>maxip[0][1]:
		maxip = [(i,signal[i])]+maxip
		
maxip2 = [y for x,y in maxip]
maxip3 = [x for x,y in maxip]

x = 0
ans = [0]*num
for i in range(0,num-1):
	while i>=maxip[x][0]:
		x += 1
	ans[i] = linearpy(maxip[x-1][0],maxip[x-1][1],maxip[x][0],maxip[x][1],i)

#plt.plot(maxip3,maxip2)
#plt.plot(signal,'r')
plt.plot(ans)
plt.show()'''
