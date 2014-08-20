# wavGen.py by WYJ
# -*- coding:utf-8 -*-
import math

inputUrl = './test.pcm'
outputUrl ='./sample.wav'

# convert 32-bit-Int into 4 bytes (little endian)
def int32toByte(d):
    r = [0,0,0,0]
    t = divmod(d,256)
    for i in range(4):
        r[i] = t[1]
        t = divmod(t[0], 256)
    return r

# convert 2-Byte into 16-bit-Int as a string
def BytetoInt16(a,b):
    lo = ord(a)
    hi = ord(b)
    if hi>>7 ==1:
        hi -= 0x100
    return str(lo + hi*0x100)

# frequency of piano key
def freqPiano(d):
    #d += 48 #in case the freq number range from 0 to 87
    return 440 * math.pow(2.0, d/12.0)

# envolope of Flute-like wave form
def envolopeFlute(d):
    thres = 0.22
    if d < thres:
        return (1-math.cos(math.pi/thres*d))/2
    elif d > 1 - thres*2:
        return (1-math.cos(math.pi/thres/2*(1-d)))/2
    else:
        return 1


# initialize wav format parameters
def wavInit():
    global dataSize
    global nchannels
    global bpsample
    global blockAlign
    global sampleps
    global header
    
    # param settings, care about dataSize & nchannels
    dataSize = 0      # size of input pcm data in Bytes
    nchannels = 2     # 1 for single; 2 for stero
    bpsample = 16     # bitsPerSample:8||16||32, 16 = size of signed short in bits
    blockAlign = bpsample/8 *nchannels # bits to Bytes, times the number of channels
    sampleps = 44100  #

    # default header
    header = [82, 73, 70, 70,      # 'RIFF'
              255, 255, 255, 255,  # dataSize+36
              87, 65, 86, 69,      # 'WAVE'
              102, 109, 116, 32,   # 'fmt '
              
              16, 0, 0, 0,         # wavSize:16||18
              1, 0, 1, 0,          # pcm:1, nchannels
              68, 172, 0, 0,       # sampleps:44100=68+172*256
              16, 177, 2, 0,       # Bps(BytesPerSecond)=sampleps*blockAlign
              2, 0, 16, 0,         # BlockAlign, bpsample
              100, 97, 116, 97,    # Bpsample
              255, 255, 255, 255]  # dataSize

# read file as binary array
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

# read file as int array
def getInt(url):
    try:
        fin = open(url, 'r')
    except:
        print "input file not exist!"
        quit()
    try:
        s = fin.read()
    finally:
        fin.close()
    return [int(i) for i in s[0:len(s)-1].split(' ')]

####################################################################
def pcm2wav():
    # read pcm file
    data = getByte(inputUrl)
    dataSize = len(data)

    print "Start converting!"
    # adjust
    header[22], header[32], header[34] = nchannels, blockAlign, bpsample
    header[4:8] = int32toByte(dataSize + 36)
    header[40:44] = int32toByte(dataSize)
    header[24:28] = int32toByte(sampleps)
    header[28:32] = int32toByte(sampleps*blockAlign)

    # generate customized header
    k = ""
    for i in header:
        k += chr(i)

    # write wav file
    fout = open(outputUrl,'wb' )
    fout.write(k)
    fout.write(data)
    fout.close()
    print "Successfully converted!"

def wav2txt():
    # read wav file
    data = getByte(inputUrl, 44)
    l = len(data)/2

    print "Start converting!"
    fout = open(outputUrl, 'w')
    for i in range (l):
        fout.write(BytetoInt16(data[i*2], data[i*2+1])+' ')
    fout.close()
    print "Successfully converted!"

####################################################################
def txt2wav():
    data = getInt(inputUrl)
    dataSize = len(data) * bpsample/8

    print "Start converting!"
    # adjust
    header[22], header[32], header[34] = nchannels, blockAlign, bpsample
    header[4:8] = int32toByte(dataSize + 36)
    header[40:44] = int32toByte(dataSize)
    header[24:28] = int32toByte(sampleps)
    header[28:32] = int32toByte(sampleps*blockAlign)

    # generate customized header
    k = ""
    for i in header:
        k += chr(i)
    fout = open(outputUrl, 'wb')
    fout.write(k)
    for i in range (len(data)):
        fout.write(chr(data[i]&0xFF)+chr((data[i]>>8)&0xFF))
    fout.close()
    print "Successfully converted!"

####################################################################
def score2wav():
    # read score file
    data = getInt(inputUrl)
    l = len(data)//2
    bufferSize = int(60.0 / data[1] * sampleps)   # sample size of one beat
    nchannels = 2
    dataSize = bufferSize * data[0] * 2 * nchannels# data[0] store the total duration in beats
    blockAlign = bpsample/8 *nchannels
    print "Start converting!"
    # adjust
    header[22], header[32], header[34] = nchannels, blockAlign, bpsample
    header[4:8] = int32toByte(dataSize + 36)
    header[40:44] = int32toByte(dataSize)
    header[24:28] = int32toByte(sampleps)
    header[28:32] = int32toByte(sampleps*blockAlign)

    # generate customized header
    k = ""
    for i in header:
        k += chr(i)
    fout = open(outputUrl, 'wb')
    fout.write(k)

    # generate wave data
    for i in range (1,l):
        amp = 4000
        w = freqPiano(data[2*i]) * 2.0 * math.pi /sampleps   #circular freq
        for j in range (bufferSize * data[2*i+1]):
            buffer = int(amp * envolopeFlute(j/float(bufferSize)/data[2*i+1]) * (math.sin(w*j) + 0.3*math.sin(w*j*2)+ 0.1* math.sin(w*j*3)))
            fout.write(chr(buffer&0xFF)+chr((buffer>>8)&0xFF))
            if (nchannels == 2):
                fout.write(chr(buffer&0xFF)+chr((buffer>>8)&0xFF))
    fout.close()
    print "Successfully converted!"

####################################################################
# main control
mode = input("select modes:\n 1: convert pcm to wav\n 2: convert wav file to array txt\n 3: convert array txt to wav file\n 4: convert score txt file to wav\n")

if mode == 1:
    inputUrl = raw_input("input the pcm file to convert: ")
    outputUrl = raw_input("output the wav file as: ")
    wavInit()
    pcm2wav()
elif mode == 2:
    inputUrl = raw_input("input the wav file to convert: ")
    outputUrl = raw_input("output the array txt file as: ")
    wav2txt()
elif mode == 3:
    inputUrl = raw_input("input the array txt file to convert: ")
    outputUrl = raw_input("output the wav file as: ")
    wavInit()
    txt2wav()
elif mode == 4:
    inputUrl = raw_input("input the score txt file to convert: ")
    outputUrl = raw_input("output the wav file as: ")
    wavInit()
    score2wav()



