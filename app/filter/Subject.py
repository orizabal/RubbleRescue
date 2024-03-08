from common import AudioItem
from reactivex.subject import Subject
from .filter import filter
from pydub import AudioSegment
from scipy.io import wavfile
import time

class ModuleSubject(Subject):    
    def __init__(self):
        super().__init__()

    def on_next(self, audioItem: AudioItem):
        print(f"Filter: Observing event from {audioItem.moduleId}")
        # Retrieve audio data from the database
        audio = AudioSegment.from_file('./audio_data/midnightRun.m4a', format='m4a')
        audio.export('./audio_data/output.wav', format='wav')
        sr, data = wavfile.read('./audio_data/output.wav')

        # Filter data
        filter(sr=sr, data=data)

        # Update row in database
        time.sleep(1)
    
        # Re-emit event to be consumed by triangulation
        print(f"Filter: Re-emitting event from {audioItem.moduleId}")
        super().on_next(audioItem)
    
    def on_error(self, err):
        print(f"Error: {err}")
    
    def on_completed(self):
        print("Filter: observer complete.")
