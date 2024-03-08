from common import AudioItem
from reactivex.subject import Subject
import time

class FilterSubject(Subject):    
    def __init__(self):
        super().__init__()

    def on_next(self, audioItem: AudioItem):
        print(f"Triangulataion: Observing event from {audioItem.moduleId}")

        # Do work
        time.sleep(1)
    
        # Re-emit event to be consumed by UI
        print(f"Triangulataion: Re-emitting event from {audioItem.moduleId}")
        super().on_next(audioItem)
    
    def on_error(self, err):
        print(f"Error: {err}")
    
    def on_completed(self):
        print("Tringulation: observer complete.")
