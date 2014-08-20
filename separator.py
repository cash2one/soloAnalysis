import numpy as np
import numpy.linalg as npl
from wavGet import signal
from tool.FFT import *

#Constants
signal = signal[:10000]
print len(signal)
N0 = (len(signal)-KAPPA)//ETA
print N0

spectrogram = np.array([STFT(signal,i) for i in range(0,N0)]).transpose()
U,s,V = npl.svd(spectrogram,full_matrices=False)
