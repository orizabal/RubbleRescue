import threading
import numpy as np
import time
import pyaudio
from scipy.io import wavfile
from queue import Queue
from scipy.optimize import minimize
from gcc_phat import gcc_phat


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
    def __init__(self, rate=16000, chunk_size=None, device_indices=None):  # sampling rate = 16000 Hz, each chunk rep 0.01s of audio at default rate, we need to provide 3 audio devices
        
        # check if there are 0 or if exactly 3 devices
        if device_indices is None or len(device_indices) != 3:
            raise ValueError("device_indices must be a list of three device indices.\n")
        
        # set up of pyaudio attributes
        self.pyaudio_instance = pyaudio.PyAudio()
        self.rate = rate
        self.sample_rate = rate
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
            # self.channels.append(max_channels)  # storing channel info 
            print(f"Device index {device_index} supports up to {max_channels} input channel(s).\n")

            # activate pyaudio and capture audio in one channel / device at sample rate and chunk size
            stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16, # 16-bit audio -> amplitude ranges from -32768 to 32767
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

    # defining the 10s window to record
    def read_fixed_duration(self, duration):
        start_time = time.time()
        data = {i: bytearray() for i in range(3)}

        while time.time() - start_time < duration:
            chunks = next(self.read_chunks())
            for i, chunk in enumerate(chunks):
                data[i].extend(chunk)

        signals = [np.frombuffer(data[i], dtype=np.int16) for i in range(3)]
        return signals

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
        tau12, _ = gcc_phat(signals[0], signals[1], fs=self.sample_rate, max_tau=MAX_TDOA, interp=1)
        tau13, _ = gcc_phat(signals[0], signals[2], fs=self.sample_rate, max_tau=MAX_TDOA, interp=1)
        tau23, _ = gcc_phat(signals[1], signals[2], fs=self.sample_rate, max_tau=MAX_TDOA, interp=1)
        
        # call DOA calculation function
        doa = self.calculate_doa(tau12, tau13, tau23, MIC_DISTANCE)
        return doa

    # calculate DOA based on single TDOA value
    def calculate_doa(self, tau12, tau13, tau23, mic_distance, sound_speed=343.2):
            # Convert TDOAs to distance differences
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
    
    def calculate_doa_coordinates(self, doa, mic_distance):
        # centroid of the microphone array equilateral triangle
        M1 = np.array([0, 0])
        M2 = np.array([mic_distance, 0])
        M3 = np.array([mic_distance / 2, mic_distance * np.sqrt(3) / 2])
        centroid = (M1 + M2 + M3) / 3

        # degrees to radians
        doa_radians = np.deg2rad(doa)

        # project the DOA from the centroid
        doa_x = centroid[0] + np.cos(doa_radians)
        doa_y = centroid[1] + np.sin(doa_radians)

        return doa_x, doa_y


# execute only when script is run directly, not imported as a module
if __name__ == '__main__':
    device_indices = [0, 3, 4] # set to airpod pro, C27, and snowball
    channels = [1, 1, 1] # all ^ devices have 1 input channel
    
    # create instance of MicArray
    with MicArray(rate=16000, chunk_size=4096, device_indices=device_indices) as mic_array:
        print("Recording for 10 seconds...")
        signals = mic_array.read_fixed_duration(10)

        start_time = time.time()
        while time.time() - start_time < 10:  # Record for 10 seconds
            chunks = next(mic_array.read_chunks())
            for i, chunk in enumerate(chunks):
                # Convert the byte data to a numpy array for processing
                signal = np.frombuffer(chunk, dtype=np.int16)
                # Calculate the audio level (you can use different metrics, here it's the max value)
                audio_level = np.max(np.abs(signal))
                # convert to dB
                max_int16 = 32768
                audio_level_db = 20 * np.log10(audio_level / max_int16)
                print(f"Audio level for microphone {i + 1}: {audio_level_db} dB")

        print("Recording complete. Processing data...\n")
        start_time = time.time()

        # calculate TDOA between pairs of microphones
        tau12, _ = gcc_phat(signals[0], signals[1], fs=16000, max_tau=MAX_TDOA)
        tau13, _ = gcc_phat(signals[0], signals[2], fs=16000, max_tau=MAX_TDOA)
        tau23, _ = gcc_phat(signals[1], signals[2], fs=16000, max_tau=MAX_TDOA)
        print(f"Time Delay between Audio 1 and 2: {tau12} seconds")
        print(f"Time Delay between Audio 2 and 3: {tau23} seconds")
        print(f"Time Delay between Audio 1 and 3: {tau13} seconds \n")

        # calculate DOA based on TDOA
        doa = mic_array.get_direction([signals[0], signals[1], signals[2]])
        doa_coordinates = mic_array.calculate_doa_coordinates(doa, MIC_DISTANCE)

        end_time = time.time()
        duration = (end_time - start_time) * 1000  # convert to ms

        print(f"Estimated DOA from Mic 1 as Reference Baseline: {doa} degrees")
        print(f"Coordinates of DOA relative to microphone array centroid: {doa_coordinates}\n")
        print(f"Processing time: {duration:.2f} ms \n")

 