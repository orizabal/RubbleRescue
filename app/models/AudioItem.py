from datetime import datetime

class AudioItem:
    id: int
    moduleId: int
    victimId: int
    recordedAt: datetime
    ref: str

    def __init__(self, id: int, moduleId: int, recordedAt: str, ref: str):
        self.id = id
        self.moduleId = moduleId
        self.recordedAt = recordedAt
        self.ref = ref

    def __init__(self, moduleId: int, victimId: int, recordedAt: str, ref: str):
        self.moduleId = moduleId
        self.victimId = victimId
        self.recordedAt = recordedAt
        self.ref = ref

    def __init__(self, id: int, moduleId: int, victimId: int, recordedAt: str, ref: str):
        self.id = id
        self.moduleId = moduleId
        self.victimId = victimId
        self.recordedAt = recordedAt
        self.ref = ref
