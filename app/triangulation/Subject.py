from typing import List
from reactivex.subject import Subject
from dao import DaoFactory
from models import AudioItem, Module, Victim
from .triangulation import triangulation
import cProfile
from pathlib import Path

class FilterSubject(Subject):    
    daoFactory = DaoFactory()
    victimDao = daoFactory.createVictimDao()
    MIC_DISTANCE = 0.23
    MAX_TDOA = MIC_DISTANCE / 343.2

    def __init__(self):
        super().__init__()

    def on_next(self, audioItems: List[AudioItem]):
        profiler = cProfile.Profile()
        profiler.enable()

        coordinates = triangulation(audioItems)

        profiler.disable()
        profiler.dump_stats(f'{Path(__file__).parent.parent}/metrics/profiling/tri.prof')
        victim = Victim(xCoordinate=coordinates[0], yCoordinate=coordinates[1])
        self.victimDao.insert(victim)
    
        # Re-emit event to be consumed by UI
        super().on_next(audioItems)
    
    def on_error(self, err):
        print(f"[FilterSubject] Error: {err}")
    
    def on_completed(self):
        print("Tringulation: observer complete.")
