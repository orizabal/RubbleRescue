class Module:
    id: int
    referencePoint: bool
    xCoordinate: float
    yCoordinate: float

    def __init__(self, id: int, referencePoint: bool, xCoordinate: float, yCoordinate: float):
        self.id = id
        self.referencePoint = referencePoint
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
