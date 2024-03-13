import numpy as np
from scipy.io import wavfile


def gcc_phat(sig, refsig, fs=1, max_tau=None, interp=16):
    '''
    This function computes the offset between the signal sig and the reference signal refsig
    using the Generalized Cross Correlation - Phase Transform (GCC-PHAT)method.
    '''

    len_sig, len_refsig = len(sig), len(refsig)
    print(f"Original length of signal: {len_sig} samples & reference signal: {len_refsig} samples")

    n = len_sig + len_refsig
    print(f"Extended length for FFT: {n}")
    
    # make sure the length for the FFT is larger or equal than len(sig) + len(refsig)
    n = sig.shape[0] + refsig.shape[0]

    # Generalized Cross Correlation Phase Transform
    SIG = np.fft.rfft(sig, n=n)
    REFSIG = np.fft.rfft(refsig, n=n)
    R = SIG * np.conj(REFSIG)

    cc = np.fft.irfft(R / np.abs(R), n=(interp * n))

    max_shift = int(interp * n / 2)
    if max_tau:
        max_shift = np.minimum(int(interp * fs * max_tau), max_shift)

    cc = np.concatenate((cc[-max_shift:], cc[:max_shift+1]))

    # find max cross correlation index
    shift = np.argmax(np.abs(cc)) - max_shift
    tau = shift / float(interp * fs)
    return tau, cc


def load_audio(file_path):
    fs, signal = wavfile.read(file_path)
    if len(signal.shape) == 2:
        signal = np.mean(signal, axis=1)  # Convert stereo to mono if necessary
    return fs, signal.astype(np.float32)



def main():
    fs1, sig1 = load_audio('audios/mic1.wav')
    fs2, sig2 = load_audio('audios/mic2.wav')
    fs3, sig3 = load_audio('audios/mic3.wav')

    if not (fs1 == fs2 == fs3):
        raise ValueError("Sample rates are not the same")

    tau12, _ = gcc_phat(sig1, sig2, fs=fs1)
    tau23, _ = gcc_phat(sig2, sig3, fs=fs2)
    tau13, _ = gcc_phat(sig1, sig3, fs=fs1)

    print(f"Time Delay between Audio 1 and 2: {tau12} seconds")
    print(f"Time Delay between Audio 2 and 3: {tau23} seconds")
    print(f"Time Delay between Audio 1 and 3: {tau13} seconds")


if __name__ == "__main__":
    main()