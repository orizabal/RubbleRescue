import os
from pathlib import Path
from reactivex import create
from datetime import datetime
from models import AudioItem, Module
from dao import DaoFactory
from .Paramiko import Paramiko
from watchdog.observers import Observer

def getArgs() -> tuple[str, str, str, str, str]:
    piHost, piUser, piDir, piPass = None, None, None, None

    piHost = str(input("Enter the host: "))
    piPort = str(input("Enter the port: "))
    piUser = str(input("Enter the user: "))
    piDir  = str(input("Enter the directory: "))
    piPass = str(input("Enter the password: "))

    return (piHost, piPort, piUser, piDir, piPass)

# This class is intended to produce events that will be consumed by
# the bandpass filter service
def produce_events(observer, scheduler):
    piHost, piPort, piUser, piDir, piPass = getArgs()
    localAudiodir = f'{Path(__file__).parent.parent.parent}/sd'
    triangle = [[3, 44.81], [6, 50], [0, 50]]
    
    # Get files from Pi
    with Paramiko(host=piHost, port=piPort, user=piUser, dir=piDir, password=piPass) as client:
        # This will run any time there is a new file added in the Pi directory
        def newFileHandler(event):
            if event.event_type == 'created':
                client.get(event.src_path, localAudiodir)

        # Initialize and start Observer (to watch Pi directory)
        observer = Observer()
        observer.schedule(newFileHandler, 'pi/path/to/audio/', recursive=True)
        observer.start()

    moduleDao = DaoFactory.createModuleDao()
    audioItemDao = DaoFactory.createAudioItemDao()
    modules = {} # physical_id: db_id
    groups = {} # time: [audio1, audio2, audio3]

    # iterate over each file in the 'SD card' directory
    for file in os.listdir(localAudiodir):
        filename = os.fsdecode(file)
        if (filename[0] == '.'): # Filter out .DS_Store..... 
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
        print("Now emitting events")
        # print(f"[ModuleEventSource] Producing event: {g}")
        observer.on_next(g) # Emit the next event
    observer.on_completed() # Indicate that no more events will be emitted


source = create(produce_events)
