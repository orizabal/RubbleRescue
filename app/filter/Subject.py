from typing import List
from reactivex.subject import Subject
import concurrent.futures
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
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)

        def processAudio(a: AudioItem):
            audio = AudioSegment.from_file(f'./audio_data/{a.ref}', format='wav')
            _, data = wavfile.read(audio)
            # Filter data
            self.metrics.trackExecutionTime(filter, 48000, data, audio)

            # update audioItem with audio
            a.ref = audio
            self.audioItemDao.update(a)
    
        for a in audioItems:
            pool.submit(processAudio(a))
    
        # Wait for threads to finish
        pool.shutdown(wait=True)
        
        # Re-emit event to be consumed by triangulation
        super().on_next(audioItems)
    
    def on_error(self, err):
        print(f"[ModuleSubject] Error: {err}")
    
    def on_completed(self):
        print("Filter: observer complete.")
