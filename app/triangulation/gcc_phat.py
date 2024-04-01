import numpy as np

# gcc_phat algorithm
def gcc_phat(sig, refsig, fs=1, max_tau=None, interp=16):
    '''
    This function computes the offset between the signal sig and the reference signal refsig
    using the Generalized Cross Correlation - Phase Transform (GCC-PHAT)method.
    '''

    # lengths of each signal
    len_sig, len_refsig = len(sig), len(refsig)
    #print(f"Original length of signal: {len_sig} samples & reference signal: {len_refsig} samples")

    # sum lengths so FFT has enough points to accommodate full length of signals when CC -> shorter length gets zeros at the end to adjust
    n = len_sig + len_refsig
    #print(f"Extended length for FFT: {n}\n")
    
    # make sure the length for the FFT is larger or equal than len(sig) + len(refsig)
    n = sig.shape[0] + refsig.shape[0]

    # Generalized Cross Correlation Phase Transform
    SIG = np.fft.rfft(sig, n=n)
    REFSIG = np.fft.rfft(refsig, n=n)
    R = SIG * np.conj(REFSIG)

    # adding epsilon so that there are no cases of dividing by 0
    epsilon = 1e-10
    cc = np.fft.irfft(R / (np.abs(R) + epsilon), n=(interp * n))

    # peak detection in CC function based on current time shift
    max_shift = int(interp * n / 2)
    if max_tau:
        max_shift = np.minimum(int(interp * fs * max_tau), max_shift)

    cc = np.concatenate((cc[-max_shift:], cc[:max_shift+1]))

    # find max cross correlation index
    shift = np.argmax(np.abs(cc)) - max_shift
    tau = shift / float(interp * fs)
    return tau, cc
