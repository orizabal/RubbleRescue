from pathlib import Path
from datetime import datetime
from time import sleep

class Metrics:
    def __init__(self, name) -> None:
        self.__logFile = Path(__file__).parent / 'log' / f'{name}.log'

    def trackExecutionTime(self, task):
        start = datetime.now()
        task()
        duration = datetime.now() - start

        with self.__logFile.open('a') as f:
            f.write(f'[{datetime.now()}] {task.__name__} complete in {duration.total_seconds()} seconds\n')

def testFunction():
    sleep(1)

if __name__ == '__main__':
    metrics = Metrics('test')
    metrics.trackExecutionTime(testFunction)
