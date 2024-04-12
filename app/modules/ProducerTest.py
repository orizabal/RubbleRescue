import os
from pathlib import Path
from reactivex import create
from datetime import datetime
from models import AudioItem, Module
from dao import DaoFactory
from .Paramiko import Paramiko
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, LoggingEventHandler
import numpy as np
from scipy.io.wavfile import write

class EventHandler(LoggingEventHandler):
    triangle = [[3, 44.81], [6, 50], [0, 50]]
    sampleRate = 16000

    def __init__(self, observer):
        self.moduleDao = DaoFactory.createModuleDao()
        self.audioItemDao = DaoFactory.createAudioItemDao()
        self.modules = {} # physical_id: db_id
        self.groups = {} # time: [audio1, audio2, audio3]
        self.observer = observer

    def dispatch(self, event: FileSystemEvent) -> None:
        print(f"Event: {event.event_type}")
        if event.event_type == 'created':
            print(f"New file: {event.src_path}")
            # client.get(event.src_path, rawAudioDir)

            filename = os.fsdecode(event.src_path).split('/')[-1].split('.')[0]
            # if (filename[0] == '.'): # Filter out .DS_Store..... 
            #     return

            # Convert RAW audio to wav
            rawAudio = np.fromfile(event.src_path, dtype=np.int16)
            write(f'{Path(__file__).parent.parent.parent}/app/audio_data/{filename}.wav', self.sampleRate, rawAudio)

            seconds, moduleId = filename.split("_")
            # insert into modules table
            if moduleId not in self.modules.keys():
                module = Module(
                    physical_id=moduleId,
                    referencePoint=True,
                    xCoordinate=self.triangle[len(self.modules)][0],
                    yCoordinate=self.triangle[len(self.modules)][1]
                )
                self.modules[moduleId] = self.moduleDao.insert(module)
            
            # insert into audio_items table
            timestamp = datetime.fromtimestamp(int(seconds))
            audioItem = AudioItem(moduleId=self.modules[moduleId], recordedAt=timestamp, ref=f'./audio_data/{filename}.wav')
            id = self.audioItemDao.insert(audioItem)
            audioItem.id = id

            # put into groups of three to be passed along the pipeline
            if timestamp not in self.groups.keys():
                self.groups[timestamp] = []
            
            self.groups[timestamp].append(audioItem)

            if len(self.groups[timestamp]) == 3:
                self.observer.on_next(self.groups[timestamp]) # Emit the next event

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
    # piHost, piPort, piUser, piDir, piPass = getArgs()
    rawAudioDir = f'{Path(__file__).parent.parent.parent}/sd'
    # wavDir = f'{Path(__file__).parent.parent.parent}/app/audio_data/'
    
    # Get files from Pi
    # with Paramiko(host=piHost, port=piPort, user=piUser, dir=piDir, password=piPass) as client:
        # This will run any time there is a new file added in the Pi directory
    # Indent this when we use Paramiko -----

    # Initialize and start Observer (to watch Pi directory)
    eventHandler = EventHandler(observer)
    watchDog = Observer()
    watchDog.schedule(eventHandler, rawAudioDir, recursive=True) # Replace './app/audio_data/' with the directory in which the Pi keeps its audio files
    watchDog.start()
    # -----

    # moduleDao = DaoFactory.createModuleDao()
    # audioItemDao = DaoFactory.createAudioItemDao()
    # modules = {} # physical_id: db_id
    # groups = {} # time: [audio1, audio2, audio3]

    # iterate over each file in the 'audio_data' directory
    # for file in os.listdir(rawAudioDir):
    #     filename = os.fsdecode(file)
    #     if (filename[0] == '.'): # Filter out .DS_Store..... 
    #         continue

    #     seconds, moduleId = filename.split("_")
    #     # insert into modules table
    #     if moduleId not in modules.keys():
    #         module = Module(
    #             physical_id=moduleId,
    #             referencePoint=True,
    #             xCoordinate=triangle[len(modules)][0],
    #             yCoordinate=triangle[len(modules)][1]
    #         )
    #         modules[moduleId] = moduleDao.insert(module)
        
    #     # insert into audio_items table
    #     timestamp = datetime.fromtimestamp(int(seconds))
    #     audioItem = AudioItem(moduleId=modules[moduleId], recordedAt=timestamp, ref=filename)
    #     id = audioItemDao.insert(audioItem)
    #     audioItem.id = id

    #     # put into groups of three to be passed along the pipeline
    #     if timestamp not in groups.keys():
    #         groups[timestamp] = []
        
    #     groups[timestamp].append(audioItem)
    
    # for g in groups.values():
    #     # print("Now emitting events")
    #     # print(f"[ModuleEventSource] Producing event: {g}")
    #     if len(g) == 3:
    #         observer.on_next(g) # Emit the next event
    # observer.on_completed() # Indicate that no more events will be emitted


source = create(produce_events)
