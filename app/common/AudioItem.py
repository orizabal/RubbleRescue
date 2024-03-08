from dataclasses import dataclass

# TODO: Remove this as we're using the DAO pattern now
@dataclass
class AudioItem:
    """Class for the item to be passed along the pipeline"""
    moduleId: str # Identifier of the physical module associated with the audio
    audioId: str # Id used to retrieve the audio data from the db

    def __init__(self, moduleId: str, audioId: str):
        self.moduleId = moduleId
        self.audioId = audioId
