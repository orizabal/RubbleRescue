from .AudioItemDaoImpl import AudioItemDaoImpl
from .ModuleDaoImpl import ModuleDaoImpl
from .NeighbourDaoImpl import NeighbourDaoImpl
from .VictimDaoImpl import VictimDaoImpl

class DaoFactory:
    @staticmethod
    def createAudioItemDao():
        return AudioItemDaoImpl()
    
    @staticmethod
    def createModuleDao():
        return ModuleDaoImpl()
    
    @staticmethod
    def createNeighbourDao():
        return NeighbourDaoImpl()
    
    @staticmethod
    def createVictimDao():
        return VictimDaoImpl()
