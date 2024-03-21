from typing import List
from reactivex.subject import Subject
from dao import DaoFactory
from models import AudioItem, Module, Victim
from .triangulation import triangulation
import random

class FilterSubject(Subject):    
    daoFactory = DaoFactory()
    victimDao = daoFactory.createVictimDao()
    MIC_DISTANCE = 0.23
    MAX_TDOA = MIC_DISTANCE / 343.2

    def __init__(self):
        super().__init__()

    def on_next(self, audioItems: List[AudioItem]):
        # print(f"Triangulataion: Observing event: {audioItems}")

        # Do work
        triangulation(audioItems)
        victim = Victim(xCoordinate=random.uniform(30.000, 80.000), yCoordinate=random.uniform(30.000, 80.000))
        self.victimDao.insert(victim)
    
        # Re-emit event to be consumed by UI
        # print(f"Triangulataion: Re-emitting event: {audioItems}")
        super().on_next(audioItems)
    
    def on_error(self, err):
        print(f"[FilterSubject] Error: {err}")
    
    def on_completed(self):
        print("Tringulation: observer complete.")
