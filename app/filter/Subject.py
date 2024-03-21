from typing import List
from reactivex.subject import Subject
from .filter import filter
from pydub import AudioSegment
from scipy.io import wavfile
from metrics import Metrics
from models import AudioItem
from dao import DaoFactory

class ModuleSubject(Subject):    
    metrics = Metrics("bandpass_filter")
    audioItemDao = DaoFactory.createAudioItemDao()

    def __init__(self):
        super().__init__()

    def on_next(self, audioItems: List[AudioItem]):
        # print(f"Filter: Observing event from: {audioItems}")
        # Retrieve audio data from the database
        for a in audioItems:
            audio = AudioSegment.from_file(f'../sd/{a.ref}', format='m4a')
            wavSrc = f'./audio_data/{a.ref.split(".")[0]}.wav'
            audio.export(wavSrc, format='wav') # This won't be needed later as files will already be in .wav
            samplingRate, data = wavfile.read(wavSrc)

            # Filter data
            self.metrics.trackExecutionTime(filter, 48000, data, wavSrc)

            # update audioItem with wavSrc
            a.ref = wavSrc
            self.audioItemDao.update(a)
    
        # Re-emit event to be consumed by triangulation
        # print(f"Filter: Re-emitting event: {audioItems}")
        super().on_next(audioItems)
    
    def on_error(self, err):
        print(f"[ModuleSubject] Error: {err}")
    
    def on_completed(self):
        print("Filter: observer complete.")
