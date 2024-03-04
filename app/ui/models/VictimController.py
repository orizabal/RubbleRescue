from PyQt6.QtCore import QObject

class VictimController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
    
    