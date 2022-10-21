import json
from json import JSONEncoder


class LocationResponse:
    def __init__(self, numberOfObjects):
        self.MapObjects = []
        self.MapObjects.append(MapObject(0, 0, "OurRobot"))
        self.MapObjects.append(MapObject(8, 2, "IndividualObstacle"))
        self.MapObjects.append(MapObject(5, 1, "OtherRobot"))


class MapObject:
    def __init__(self, x, y, mapobjtype):
        self.Location = (x, y)
        self.MapObjectType = mapobjtype


class LocationResponseEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
