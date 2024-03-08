class Neighbour:
    moduleId: int
    neighbourModuleId: int

    def __init__(self, moduleId: int, neighbourModuleId: int):
        self.moduleId = moduleId
        self.neighbourModuleId = neighbourModuleId
