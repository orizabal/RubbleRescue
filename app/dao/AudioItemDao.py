from abc import ABC, abstractmethod
from models import AudioItem

# AudioItem DAO Interface
class AudioItemDao(ABC):
    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def insert(self, audioItem: AudioItem):
        pass

    @abstractmethod
    def update(self, audioItem: AudioItem):
        pass

    @abstractmethod
    def delete(self, audioItem: AudioItem):
        pass
