'''from __future__ import division
import tool.normalizer as nml
import struct
import tool.denoiser as dn
file = open(raw_input(), 'rb')

#META_INFO process
META = struct.unpack('5i',file.read(20))
if META[-1]==16:
	tmpInfo = ('2h2i2h2i',24)
else:
	tmpInfo = ('2h2i3h2i',26)
META += struct.unpack(tmpInfo[0],file.read(tmpInfo[1]))
if struct.pack('i',META[-2])=="fact":
	META += struct.unpack('3i',file.read(12))

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
#signal = dn.GFilter(signal,15)'''

import tool.normalizer as nml
import tool.denoiser as dn
import math

def BytetoInt16(a,b):
    lo = ord(a)
    hi = ord(b)
    if hi>>7 ==1:
        hi -= 0x100
    return str(lo + hi*0x100)
	
def getByte(url, offset = 0):
    try:
        fin = open(url, 'rb')
    except:
        print "input file not exist!"
        quit()
    try:
        fin.seek(offset)
        s = fin.read()
    finally:
        fin.close()
    return s

def get(url):
	data = getByte(url, 44)
	signal = [int(BytetoInt16(data[i*2], data[i*2+1])) for i in range(len(data)/2)]
	signal = nml.max_normalize(signal)
	return signal
#signal = dn.GFilter(signal,15)
