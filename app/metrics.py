from pathlib import Path
from datetime import datetime

class Metrics:
    def __init__(self, name) -> None:
        self.__logFile = Path(__file__).parent / 'log' / f'{name}.log'

    def trackExecutionTime(self, task, *args):
        start = datetime.now()
        task(*args)
        duration = datetime.now() - start

        with self.__logFile.open('a') as f:
            f.write(f'[{datetime.now()}] {task.__name__} complete in {duration.total_seconds() * 1000} milliseconds\n')
