from typing import List
from reactivex.subject import Subject
from dao import DaoFactory
from models import Victim
import random

class FilterSubject(Subject):    
    daoFactory = DaoFactory()
    victimDao = daoFactory.createVictimDao()

    def __init__(self):
        super().__init__()

    def on_next(self, audioItems: List[str]):
        print(f"Triangulataion: Observing event: {audioItems}")

        # Do work
        victim = Victim(xCoordinate=random.uniform(30.000, 80.000), yCoordinate=random.uniform(30.000, 80.000))
        self.victimDao.insert(victim)
    
        # Re-emit event to be consumed by UI
        print(f"Triangulataion: Re-emitting event: {audioItems}")
        super().on_next(audioItems)
    
    def on_error(self, err):
        print(f"[FilterSubject] Error: {err}")
    
    def on_completed(self):
        print("Tringulation: observer complete.")
