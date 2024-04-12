from typing import List
from reactivex.subject import Subject
import concurrent.futures
from .filter import filter
from pydub import AudioSegment
from scipy.io import wavfile
from metrics import Metrics
from models import AudioItem
from dao import DaoFactory
import cProfile
from pathlib import Path

class ModuleSubject(Subject):    
    metrics = Metrics("multithreaded_filter")
    audioItemDao = DaoFactory.createAudioItemDao()

    def __init__(self):
        super().__init__()

    def on_next(self, audioItems: List[AudioItem]):
        def processAudio(k, v):
            filter(48000, v, k)
        
        profiler = cProfile.Profile()
        profiler.enable()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            dataList = {}
            for a in audioItems:
                _, data = wavfile.read(a.ref)
                dataList[a.ref] = data

            executor.map(processAudio, dataList.items())
            executor.shutdown(wait=True)

        profiler.disable()
        profiler.dump_stats(f'{Path(__file__).parent.parent}/metrics/profiling/filter.prof')

        # Re-emit event to be consumed by triangulation
        super().on_next(audioItems)
    
    def on_error(self, err):
        print(f"[ModuleSubject] Error: {err}")
    
    def on_completed(self):
        print("Filter: observer complete.")
