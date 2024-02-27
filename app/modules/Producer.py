from common import AudioItem
from reactivex import create
import time

# This class is intended to produce events that will be consumed by
# the bandpass filter service
def produce_events(observer, scheduler):
    for i in range(3):
        time.sleep(1)
        print(f"Module: Producing event {i}")
        audioItem = AudioItem(moduleId=f"module_{i}", audioId=f"audio_{i}")
        observer.on_next(audioItem) # Emit the next event
    observer.on_completed() # Indicte that no more events will be emitted


source = create(produce_events)
