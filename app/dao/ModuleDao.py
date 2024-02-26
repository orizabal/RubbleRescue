from abc import ABC, abstractmethod
from models import Module

class ModuleDao(ABC):
    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def insert(self, module: Module):
        pass

    @abstractmethod
    def update(self, module: Module):
        pass

    @abstractmethod
    def delete(self, module: Module):
        pass
