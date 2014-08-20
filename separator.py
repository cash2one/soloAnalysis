import numpy as np
import numpy.linalg as npl
from wavGet import signal
from tool.FFT import *

#Constants
N0 = (len(signal)-KAPPA)//ETA

spectrogram = np.array([STFT(signal,i) for i in range(0,N0)]).transpose()
U,s,V = npl.svd(spectrogram,full_matrices=False)
