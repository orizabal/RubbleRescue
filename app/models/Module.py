class Module:
    id: int
    physical_id: str
    referencePoint: bool
    xCoordinate: float
    yCoordinate: float

    def __init__(self, id: int, physical_id: str, referencePoint: bool, xCoordinate: float, yCoordinate: float):
        self.id = id
        self.physical_id: physical_id
        self.referencePoint = referencePoint
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
    
    def __init__(self, physical_id: str, referencePoint: bool, xCoordinate: float, yCoordinate: float):
        self.physical_id: physical_id
        self.referencePoint = referencePoint
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
