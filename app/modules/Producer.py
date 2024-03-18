import os
from reactivex import create
import random
import time
from datetime import datetime
from models import AudioItem, Module, Neighbour
from dao import DaoFactory

# This class is intended to produce events that will be consumed by
# the bandpass filter service
def produce_events(observer, scheduler):
    dir = os.fsdecode('../sd')
    moduleDao = DaoFactory.createModuleDao()
    audioItemDao = DaoFactory.createAudioItemDao()
    modules = {} # physical_id: db_id
    groups = {} # time: [audio1, audio2, audio3]

    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        seconds, moduleId = filename.split("_")
        # insert into modules table
        if moduleId not in modules.keys():
            module = Module(
                physical_id=moduleId,
                referencePoint=True,
                xCoordinate=60.3422 + float(random.randint(0, 20)),
                yCoordinate=40.1232 + float(random.randint(0, 20))
            )
            modules[moduleId] = moduleDao.insert(module)
        
        # insert into audio_items table
        timestamp = datetime.fromtimestamp(int(seconds))
        audioItem = AudioItem(moduleId=modules[moduleId], recordedAt=timestamp, ref=filename)
        audioItemDao.insert(audioItem)

        # put into groups of three to be passed along the pipeline
        if timestamp not in groups.keys():
            groups[timestamp] = []
        
        groups[timestamp].append(filename)
    
    for g in groups.values():
        print(f"[ModuleEventSource] Producing event: {g}")
        observer.on_next(g) # Emit the next event
    observer.on_completed() # Indicte that no more events will be emitted


source = create(produce_events)
