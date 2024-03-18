class Victim:
    id: int
    xCoordinate: float
    yCoordinate: float
    truePositive: bool = False
    locationChecked: bool = False

    def __init__(self, id):
        self.id = id
    
    def __init__(self, xCoordinate: float, yCoordinate: float):
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
