import threading
import numpy as np
import math
import pyaudio
from queue import Queue
from scipy.optimize import minimize
from gcc_phat import gcc_phat



# things left to do:
# - adjust DOA so that it works bc rn calculate_doa function is not being defined properly
# - make it start when user presses 'enter' to collect the 10s from hardware, then itll stop the streams after 10s



# adjust values based on your microphone array's geometry
MIC_DISTANCE = 0.23  # distance between microphones in meters (change later -> currently 8 inches)
MAX_TDOA = MIC_DISTANCE / 343.2  # max TDOA btwn 2 mics  -> defines upper bound for TDOA accuracy


# listing out all audio devices connected to laptop and their I/O channels
def list_audio_devices():
    p = pyaudio.PyAudio()
    print("Available audio devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']}")
        print(f"  - Max Input Channels: {device_info['maxInputChannels']}")
        print(f"  - Max Output Channels: {device_info['maxOutputChannels']}")
        print(f"  - Default Sample Rate: {device_info['defaultSampleRate']}\n")
    p.terminate()

list_audio_devices()


# to handle audio input from 3 mics, process audio data, and estimate DOA of sound source
class MicArray(object):

    #initializes an instance of MicArray to handle audio input from the 3 mics
    def __init__(self, rate=16000, chunk_size=None, device_indices=None):  # sampling rate = 16000 Hz, each chunk rep 0.0s of audio at default rate, we need to provide 3 audio devices
        
        # check if there are 0 or if exactly 3 devices
        if device_indices is None or len(device_indices) != 3:
            raise ValueError("device_indices must be a list of three device indices.\n")
        
        # set up of pyaudio attributes
        self.pyaudio_instance = pyaudio.PyAudio()
        self.rate = rate
        self.chunk_size = chunk_size if chunk_size else rate // 100
        self.device_indices = device_indices
        self.queues = [Queue() for _ in range(3)]
        self.quit_events = [threading.Event() for _ in range(3)]
        self.streams = []
        self.channels = []

        # setting up each individual audio device (3 of them)
        for i, device_index in enumerate(device_indices):
            dev_info = self.pyaudio_instance.get_device_info_by_index(device_index)
            max_channels = dev_info['maxInputChannels']
            self.channels.append(max_channels)  # storing channel info 
            print(f"Device index {device_index} supports up to {max_channels} input channel(s). Using 1 channel for this device.")

            # activate pyaudio and capture audio in one channel / device at sample rate and chunk size
            stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=1,  # Use only one channel for each device
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                input_device_index=device_index,
                stream_callback=self._make_callback(self.queues[i], self.quit_events[i])
            )
            self.streams.append(stream)  # created pyaudio stream is appended 

    # whenever there is new audio data available from a pyaudio device stream
    def _make_callback(self, queue, quit_event):
        def callback(in_data, frame_count, time_info, status):
            if not quit_event.is_set():
                queue.put(in_data)
            return None, pyaudio.paContinue
        return callback

    # initiate audio streaming for each audio input stream
    def start(self):
        for stream in self.streams:
            stream.start_stream()

    # stop audio capture for each stream 
    def stop(self):
        for event in self.quit_events:
            event.set()

        for stream in self.streams:
            stream.stop_stream()
            stream.close()

    # gets audio data chunks from each mic in real-time
    def read_chunks(self):
        while not all(event.is_set() for event in self.quit_events):
            yield [q.get() for q in self.queues]

    # start audio streams for each mic -> to be used below in 'with MicArray'
    def __enter__(self):
        self.start()
        return self  # allows instance of MicArray to eb assigned to a variable in the 'with' statement

    # stops MicArray instance - halting all audio streams
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.pyaudio_instance.terminate()

    # for TDOA calculations of an equilateral triangle
    def get_direction(self, buf):
        # calling gcc_phat function to calculate TDOA between each pair defined
        tau12, _ = gcc_phat(buf[0::3], buf[1::3], fs=self.sample_rate, max_tau=MAX_TDOA, interp=1)
        tau13, _ = gcc_phat(buf[0::3], buf[2::3], fs=self.sample_rate, max_tau=MAX_TDOA, interp=1)
        tau23, _ = gcc_phat(buf[1::3], buf[2::3], fs=self.sample_rate, max_tau=MAX_TDOA, interp=1)
        
        # call DOA calculation function
        doa = self.calculate_doa(tau12, tau13, tau23, MIC_DISTANCE)
        return doa

    # calculate DOA based on singel TDOA value
    def calculate_doa(self, tau12, tau13, tau23, mic_distance, sound_speed=343.2):
            # Ccnvert TDOAs to distance differences
            d1 = mic_distance 
            d2 = d1 - tau12 * sound_speed
            d3 = d1 - tau13 * sound_speed

            # Microphone positions
            M1 = np.array([0, 0])
            M2 = np.array([mic_distance, 0])
            M3 = np.array([mic_distance / 2, mic_distance * np.sqrt(3) / 2])

            # objective function: sum of squared differences between expected and actual distances
            def objective_function(S):
                d1_est = np.linalg.norm(S - M1)
                d2_est = np.linalg.norm(S - M2)
                d3_est = np.linalg.norm(S - M3)
                return (d1_est - d1)**2 + (d2_est - d2)**2 + (d3_est - d3)**2

            # initial guess for the source position (can be the centroid of the triangle for a starting point)
            initial_guess = (M1 + M2 + M3) / 3

            # optimization
            result = minimize(objective_function, initial_guess, method='L-BFGS-B')

            # estimated source position
            S_est = result.x

            # assuming DOA is the angle between the positive x-axis and the line connecting M1 and the source
            doa = np.arctan2(S_est[1], S_est[0]) * (180.0 / np.pi)
            return doa if doa >= 0 else doa + 360
    

# capture audio data from 3 mics, TDOA btwn pairs of mics, DOA based on TDOAs
with MicArray(rate=16000, chunk_size=4096, device_indices=[0, 4, 5]) as mic_array:
    for chunks in mic_array.read_chunks():
        # convert byte data to numpy arrays for processing
        sig1 = np.frombuffer(chunks[0], dtype=np.int16)
        sig2 = np.frombuffer(chunks[1], dtype=np.int16)
        sig3 = np.frombuffer(chunks[2], dtype=np.int16)

        # calculate TDOA between pairs of microphones.
        tau12, _ = gcc_phat(sig1, sig2, fs=16000)
        tau23, _ = gcc_phat(sig2, sig3, fs=16000)
        tau13, _ = gcc_phat(sig1, sig3, fs=16000)
        print(f"Time Delay between Audio 1 and 2: {tau12} seconds")
        print(f"Time Delay between Audio 1 and 3: {tau13} seconds")
        print(f"Time Delay between Audio 2 and 3: {tau23} seconds")

        # calculate DOA based on TDOA - ADJUST FORMULA/ARGUMENTS
        doa12 = self.calculate_doa(tau12, MIC_DISTANCE)
        doa23 = self.calculate_doa(tau23, MIC_DISTANCE)
        doa13 = self.calculate_doa(tau13, MIC_DISTANCE)
        print(f"DOA between Mic 1 and Mic 2: {doa12} degrees")
        print(f"DOA between Mic 2 and Mic 3: {doa23} degrees")
        print(f"DOA between Mic 1 and Mic 3: {doa13} degrees")


# execute only when script is run directly, not imported as a module
if __name__ == '__main__':
    device_indices = [0, 4, 5] # set to airpod pro, C27, and snowball
    channels = [1, 1, 1] # all ^ devices have 1 input channel

    # create instance of MicArray
    with MicArray(rate=16000, chunk_size=4096, device_indices=device_indices, channels=channels) as mic_array:
        for chunks in mic_array.read_chunks():
            # chunks[0] is the data from the first device, chunks[1] from the second, etc
            print(chunks) 