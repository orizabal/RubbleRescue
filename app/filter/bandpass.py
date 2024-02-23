import matplotlib.pyplot as plt
import numpy as np

from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import ellip, freqz, lfilter, butter

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
    b, a = ellip_bandpass(order=order, rp=rp, rs=rs, lowcut=lowcut, highcut=highcut, fs=fs)
    y = lfilter(b, a, data)
    return y


def main():
    # filter values from Matlab
    order = 6

    # In Hz
    fstop1 = 100
    fpass2 = 17000

    # Make some data to be filtered
    audio = AudioSegment.from_file('./data/midnightRun.m4a', format='m4a')
    audio.export('output.wav', format='wav')
    sr, data = wavfile.read('./data/output.wav')

    # Get filter coeffs to plot freq response
    b, a = ellip_bandpass(order=order, rp=0.05, rs=100, lowcut=fstop1, highcut=fpass2, fs=sr)

    # Plot frequency response
    w, h = freqz(b, a, fs=sr)

    plt.subplot(2, 1, 1)
    plt.plot(w, np.abs(h), 'b')
    plt.axvline(fstop1, color='r', linestyle='--')
    plt.axvline(fpass2, color='r', linestyle='--')
    plt.xlim(-1000, sr/2.1)
    plt.title("Bandpass Filter Frequency Response")
    plt.xlabel('Frequency [Hz]')
    plt.grid()

    # Filter data
    y = bandpass_filter(order=order, rp=0.05, rs=100, lowcut=fstop1, highcut=fpass2, fs=sr, data=data)
    length = data.shape[0] / sr
    t = np.linspace(0., length, data.shape[0])
    plt.subplot(2, 1, 2)
    plt.plot(t, data, '-b', label='data')
    plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
    plt.xlabel('Time [sec]')
    plt.grid()
    plt.legend()

    plt.subplots_adjust(hspace=0.35)

    plt.show()


if __name__ == "__main__":
    main()

