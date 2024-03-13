from queue import Queue
import threading
import numpy as np
from gcc_phat import gcc_phat
import math
import pyaudio


SOUND_SPEED = 343.2

# MIC_DISTANCE_6P1 = 0.064
# MAX_TDOA_6P1 = MIC_DISTANCE_6P1 / float(SOUND_SPEED)

# MIC_DISTANCE_4 = 0.08127
# MAX_TDOA_4 = MIC_DISTANCE_4 / float(SOUND_SPEED)

# Adjust these values based on your microphone array's geometry
MIC_DISTANCE = 0.1  # Distance between microphones in meters (example value)
MAX_TDOA = MIC_DISTANCE / SOUND_SPEED


class MicArray(object):

    def __init__(self, rate=16000, channels=8, chunk_size=None):
        self.pyaudio_instance = pyaudio.PyAudio()
        self.queue = Queue.Queue()
        self.quit_event = threading.Event()
        self.channels = channels
        self.sample_rate = rate
        self.chunk_size = chunk_size if chunk_size else rate / 100

        device_index = None
        for i in range(self.pyaudio_instance.get_device_count()):
            dev = self.pyaudio_instance.get_device_info_by_index(i)
            name = dev['name'].encode('utf-8')
            print(i, name, dev['maxInputChannels'], dev['maxOutputChannels'])
            if dev['maxInputChannels'] == self.channels:
                print('Use {}'.format(name))
                device_index = i
                break

        if device_index is None:
            raise Exception('can not find input device with {} channel(s)'.format(self.channels))

        self.stream = self.pyaudio_instance.open(
            input=True,
            start=False,
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=int(self.sample_rate),
            frames_per_buffer=int(self.chunk_size),
            stream_callback=self._callback,
            input_device_index=device_index,
        )

    def _callback(self, in_data, frame_count, time_info, status):
        self.queue.put(in_data)
        return None, pyaudio.paContinue

    def start(self):
        self.queue.queue.clear()
        self.stream.start_stream()


    def read_chunks(self):
        self.quit_event.clear()
        while not self.quit_event.is_set():
            frames = self.queue.get()
            if not frames:
                break

            frames = np.fromstring(frames, dtype='int16')
            yield frames

    def stop(self):
        self.quit_event.set()
        self.stream.stop_stream()
        self.queue.put('')

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        if value:
            return False
        self.stop()

    def get_direction(self, buf):
        # For a 3-mic array, you need to define how you want to calculate the DOA based on the TDOAs
        # between the microphone pairs. This is a placeholder implementation.
        tau12, _ = gcc_phat(buf[0::3], buf[1::3], fs=self.sample_rate, max_tau=MAX_TDOA, interp=1)
        tau13, _ = gcc_phat(buf[0::3], buf[2::3], fs=self.sample_rate, max_tau=MAX_TDOA, interp=1)
        tau23, _ = gcc_phat(buf[1::3], buf[2::3], fs=self.sample_rate, max_tau=MAX_TDOA, interp=1)
        
        # Placeholder: calculate and return the DOA based on the TDOAs
        # You will need to replace this with your specific geometry-based DOA calculation
        return tau12, tau13, tau23



def test_3mic():
    import signal
    import time

    is_quit = threading.Event()

    def signal_handler(sig, num):
        is_quit.set()
        print('Quit')

    signal.signal(signal.SIGINT, signal_handler)

    with MicArray(16000, 3, 16000 / 4) as mic:
        for chunk in mic.read_chunks():
            taus = mic.get_direction(chunk)
            print(taus)  # Replace this with your DOA calculation

            if is_quit.is_set():
                break



if __name__ == '__main__':
    test_3mic()
