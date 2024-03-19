import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(f'{os.getcwd()}/filter')

from filter import filter

# create a signal
samplingFrequency = 48000
t = np.linspace(0, 1, samplingFrequency, endpoint=False) # time vector
signalFrequency = 8000
signalAmplitude = 1
signalWave = signalAmplitude * np.sin(2 * np.pi * signalFrequency * t)

# add noise to the signal
noiseAmplitude = 0.5
noise = noiseAmplitude * np.random.randn(len(signalWave))
noisySignal = signalWave + noise

# filter the noisy signal
filteredSignal = filter(samplingFrequency, noisySignal, '')

# measure signal power of filtered signal
signalPower = np.mean(filteredSignal**2)

# measure noise power
noisePower = np.mean(noise**2)

# calculate signal-to-noise ratio (SNR) in dB
snr = 10 * np.log10(signalPower / noisePower)

print(snr)
