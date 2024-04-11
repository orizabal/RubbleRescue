from typing import List
from reactivex.subject import Subject
import concurrent.futures
from .filter import filter
from pydub import AudioSegment
from scipy.io import wavfile
from metrics import Metrics
from models import AudioItem
from dao import DaoFactory
import threading

class ModuleSubject(Subject):    
    metrics = Metrics("multithreaded_filter")
    audioItemDao = DaoFactory.createAudioItemDao()

    def __init__(self):
        super().__init__()

    def on_next(self, audioItems: List[AudioItem]):
        def processAudio(a: AudioItem):
            audioPath = f'./audio_data/{a.ref}.wav'
            _, data = wavfile.read(audioPath)
            # Filter data
            filter(48000, data, audioPath)

            # update audioItem with audio
            a.ref = audioPath
            self.audioItemDao.update(a)

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            def threaded():
                executor.map(processAudio, audioItems)
                executor.shutdown(wait=True)

            self.metrics.trackExecutionTime(threaded)
        
        # Re-emit event to be consumed by triangulation
        super().on_next(audioItems)
    
    def on_error(self, err):
        print(f"[ModuleSubject] Error: {err}")
    
    def on_completed(self):
        print("Filter: observer complete.")
