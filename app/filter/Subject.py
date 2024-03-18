from typing import List
from reactivex.subject import Subject
from .filter import filter
from pydub import AudioSegment
from scipy.io import wavfile

class ModuleSubject(Subject):    
    def __init__(self):
        super().__init__()

    def on_next(self, audioItems: List[str]):
        print(f"Filter: Observing event from: {audioItems}")
        # Retrieve audio data from the database
        for idx, a in enumerate(audioItems):
            audio = AudioSegment.from_file(f'../sd/{a}', format='m4a')
            wavSrc = f'./audio_data/{a.split(".")[0]}.wav'
            audio.export(wavSrc, format='wav') # This won't be needed later as files will already be in .wav
            samplingRate, data = wavfile.read(wavSrc)

            # Filter data
            filter(sr=samplingRate, data=data, source=wavSrc)

            # update source path for re-emit
            audioItems[idx] = wavSrc
    
        # Re-emit event to be consumed by triangulation
        print(f"Filter: Re-emitting event: {audioItems}")
        super().on_next(audioItems)
    
    def on_error(self, err):
        print(f"[ModuleSubject] Error: {err}")
    
    def on_completed(self):
        print("Filter: observer complete.")
