from .AudioItemDao import AudioItemDao
from models import AudioItem

class AudioItemDaoImpl(AudioItemDao):
    def find_by_id(self, id):
        pass

    def get_all(self):
        pass

    def insert(self, audioItem: AudioItem):
        pass

    def update(self, audioItem: AudioItem):
        pass

    def delete(self, audioItem: AudioItem):
        pass
