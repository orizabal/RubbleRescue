import os
from pathlib import Path
from reactivex import create
from datetime import datetime
from models import AudioItem, Module
from dao import DaoFactory

# This class is intended to produce events that will be consumed by
# the bandpass filter service
def produce_events(observer, scheduler):
    dir = f'{Path(__file__).parent.parent.parent}/sd'
    moduleDao = DaoFactory.createModuleDao()
    audioItemDao = DaoFactory.createAudioItemDao()
    modules = {} # physical_id: db_id
    groups = {} # time: [audio1, audio2, audio3]

    triangle = [[3, 44.81], [6, 50], [0, 50]]

    # iterate over each file in the 'SD card' directory
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if (filename[0] == '.'): # Filter out .DS_Store...
            continue

        seconds, moduleId = filename.split("_")
        # insert into modules table
        if moduleId not in modules.keys():
            module = Module(
                physical_id=moduleId,
                referencePoint=True,
                xCoordinate=triangle[len(modules)][0],
                yCoordinate=triangle[len(modules)][1]
            )
            modules[moduleId] = moduleDao.insert(module)
        
        # insert into audio_items table
        timestamp = datetime.fromtimestamp(int(seconds))
        audioItem = AudioItem(moduleId=modules[moduleId], recordedAt=timestamp, ref=filename)
        id = audioItemDao.insert(audioItem)
        audioItem.id = id

        # put into groups of three to be passed along the pipeline
        if timestamp not in groups.keys():
            groups[timestamp] = []
        
        groups[timestamp].append(audioItem)
    
    for g in groups.values():
        observer.on_next(g) # Emit the next event
    observer.on_completed() # Indicate that no more events will be emitted


source = create(produce_events)
