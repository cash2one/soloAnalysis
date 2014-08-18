from __future__ import division
import tool.normalizer as nml
import struct
import tool.denoiser as dn
file = open(raw_input(), 'rb')

#META_INFO process
META = struct.unpack('5l',file.read(20))
if META[-1]==16:
	tmpInfo = ('2h2l2h2l',24)
else:
	tmpInfo = ('2h2l3h2l',26)
META += struct.unpack(tmpInfo[0],file.read(tmpInfo[1]))
if struct.pack('l',META[-2])=="fact":
	META += struct.unpack('3l',file.read(12))

Channels,BitsPerSample = META[6],META[10]
LChannel,RChannel,signal = [],[],[]
SampleNum = META[-1]//16

#extract DATA
if Channels==2 and BitsPerSample==16:
	for samples in range(0,SampleNum):
		LChannel += [struct.unpack('q',file.read(8))[0]]
		RChannel += [struct.unpack('q',file.read(8))[0]]
		signal += [(LChannel[-1]+RChannel[-1])/2]
	
signal = nml.max_normalize(signal)
signal = dn.GFilter(signal,15)
