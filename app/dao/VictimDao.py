from abc import ABC, abstractmethod
from models import Victim

class VictimDao(ABC):
    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def insert(self, victim: Victim):
        pass

    @abstractmethod
    def update(self, victim: Victim):
        pass

    @abstractmethod
    def delete(self, victim: Victim):
        pass
