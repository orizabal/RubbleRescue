from typing import List
from reactivex.subject import Subject
import time

class FilterSubject(Subject):    
    def __init__(self):
        super().__init__()

    def on_next(self, audioItems: List[str]):
        print(f"Triangulataion: Observing event: {audioItems}")

        # Do work
        time.sleep(1)
    
        # Re-emit event to be consumed by UI
        print(f"Triangulataion: Re-emitting event: {audioItems}")
        super().on_next(audioItems)
    
    def on_error(self, err):
        print(f"[FilterSubject] Error: {err}")
    
    def on_completed(self):
        print("Tringulation: observer complete.")
