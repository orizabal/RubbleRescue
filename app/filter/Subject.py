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
    modulesDao = DaoFactory.createModuleDao()

    def __init__(self):
        super().__init__()

    def on_next(self, emittedPair, emit):
        metrics = Metrics("multithreaded_filter")
        # audioItemDao = DaoFactory.createAudioItemDao()

        # Emit new modules
        dbModules = self.modulesDao.get_all()
        modules = []
        for m in dbModules:
            modules.append({
                'id': m[0],
                'xCoordinate': m[2],
                'yCoordinate': m[3]
            })
        
        emit('newModules', {'modules': modules})

        def processAudio(k, v):
            filter(16000, v, k)
        
        profiler = cProfile.Profile()
        profiler.enable()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            dataList = {}
            for a in emittedPair[0]:
                _, data = wavfile.read(a.ref)
                dataList[a.ref] = data
            
            def threadedFilter():
                for k, v in dataList.items():
                    executor.submit(processAudio, k, v)
                # executor.map(processAudio, dataList.items())
                executor.shutdown(wait=True)
            
            metrics.trackExecutionTime(threadedFilter)

        profiler.disable()
        profiler.dump_stats(f'{Path(__file__).parent.parent}/metrics/profiling/filter.prof')

        # Re-emit event to be consumed by triangulation
        super().on_next(emittedPair[0])
    
    def on_error(self, err):
        print(f"[ModuleSubject] Error: {err}")
    
    def on_completed(self):
        print("Filter: observer complete.")
