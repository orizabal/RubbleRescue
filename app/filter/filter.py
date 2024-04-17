import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import ellip, lfilter # , freqz
import scipy.io.wavfile as wavf

def ellip_bandpass(order, rp, rs, lowcut, highcut, fs):
    # params:
    # N (int) = order of the filter
    # rp (float) = max ripple allowed below unity gain in the passband. In decibels, +ve number
    # Wn (array) = For elliptic filtes, this is the point in the transition band at which
        # the gain first drops below -rp
    # btype = Type of filter
    b, a = ellip(N=order, rp=rp, rs=rs, Wn=[lowcut, highcut], fs=fs, btype='band')
    return b, a


def bandpass_filter(order, rp, rs, lowcut, highcut, fs, data):
    # b, a = ellip_bandpass(order=order, rp=rp, rs=rs, lowcut=lowcut, highcut=highcut, fs=fs)
    b = [-0.079795555662058162416094830859947251156, -0.001948674964559762856630698024673620239, -0.089775601349694311714699779258808121085,  0.007868104314545681932102638711512554437, -0.141883262108245894461688862975279334933,  0.056459639538432249139532359549775719643, -0.277399898077907880455938993691233918071,  0.564580352216893510686190893466118723154,  0.564580352216893510686190893466118723154, -0.277399898077907880455938993691233918071,  0.056459639538432249139532359549775719643, -0.141883262108245894461688862975279334933,  0.007868104314545681932102638711512554437, -0.089775601349694311714699779258808121085, -0.001948674964559762856630698024673620239, -0.079795555662058162416094830859947251156]
    a = []
    # print(f'b = {b}, a = {a}')
    y = lfilter(b, a, data)
    return y


def filter(sr: int, data, source: str):
    # filter values from Matlab
    order = 8

    # In Hz
    fstop1 = 100
    fpass2 = 7500

    # Get filter coeffs to plot freq response
    # b, a = ellip_bandpass(order=order, rp=0.05, rs=100, lowcut=fstop1, highcut=fpass2, fs=sr)

    # Plot frequency response
    # w, h = freqz(b, a, fs=sr)

    # plt.subplot(3, 1, 1)
    # plt.plot(w, np.abs(h), 'b')
    # plt.axvline(fstop1, color='r', linestyle='--')
    # plt.axvline(fpass2, color='r', linestyle='--')
    # plt.xlim(-1000, sr/2.1)
    # plt.title("Bandpass Filter Frequency Response")
    # plt.xlabel('Frequency [Hz]')
    # plt.grid()

    # Filter data
    y = bandpass_filter(order=order, rp=0.05, rs=100, lowcut=fstop1, highcut=fpass2, fs=sr, data=data)
    # length = data.shape[0] / sr
    # t = np.linspace(0., length, data.shape[0])
    # plt.subplot(3, 1, 2)
    # plt.plot(t, data, '-b', label='data')
    # plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
    # plt.xlabel('Time [sec]')
    # plt.grid()
    # plt.legend()

    # plt.subplots_adjust(hspace=0.35)

    # plt.show()

    # update the wav file with the filtered audio
    wavf.write(source, sr, y)
    # return y
