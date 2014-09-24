soloAnalysis
============

This repository gives the analysis to one-source sound clips, fetch its rythm, pitches and evaluate its tonal quality.

structure
---
+ `tool`: including denoiser.py, FFT.py, normalizer.py, implementing basic signal processing function;
+ `wavGen.py`: the python version of wavGen, provide several basic conversion between .wav file and others;
+ `wavGet.py`: a simpler version of wavGen, purposing for convert .wav file to wave array normalized into range [-1,1];
+ `envelope.py`: Find the envelope of a wave. The output is an array of length 100, which is the equidistant sampling of the envelope curve;
+ `separator.py`: The core file. NMF separates the wave curve from wavGet.py, into r parts. A is a matrix of n\times r, whose each column is the frequency domain information of one part; S is a matrix of r\times m, which is a coefficient matrix denoting the amplitude of each part on each time bin.
+ `feature.py`: to combine the output of envelope and separator to form the final feature of a sound segment;

FAQ
---
