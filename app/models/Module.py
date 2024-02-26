class Module:
    id: int
    static: bool
    xCoordinate: float
    yCoordinate: float

    def __init__(self, id: int, static: bool, xCoordinate: float, yCoordinate: float):
        self.id = id
        self.static = static
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
