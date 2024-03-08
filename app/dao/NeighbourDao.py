from abc import ABC, abstractmethod
from models import Neighbour

class NeighbourDao(ABC):
    @abstractmethod
    def get_all_neighbours(self, id):
        pass
