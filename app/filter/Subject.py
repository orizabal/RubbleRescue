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
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)

        def processAudio(a: AudioItem):
            # print(f"Thread {threading.current_thread().ident} filtering audio")
            # audio = AudioSegment.from_file(f'./audio_data/{a.ref}.wav', format='wav')
            audioPath = f'./audio_data/{a.ref}.wav'
            _, data = wavfile.read(audioPath)
            # Filter data
            filter(48000, data, audioPath)

            # update audioItem with audio
            a.ref = audioPath
            self.audioItemDao.update(a)
        
        def threadedProcess():
            for a in audioItems:
                pool.submit(processAudio(a))

            # Wait for threads to finish
            pool.shutdown(wait=True)

        self.metrics.trackExecutionTime(threadedProcess)
        
        # Re-emit event to be consumed by triangulation
        super().on_next(audioItems)
    
    def on_error(self, err):
        print(f"[ModuleSubject] Error: {err}")
    
    def on_completed(self):
        print("Filter: observer complete.")
