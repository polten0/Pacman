from ObjectClasses.Objects import MapObject
import os

class Wall(MapObject):
    def __init__(self):
        super().__init__()
        self.isCollide = True

class Floor(MapObject):
    def __init__(self):
        super().__init__()
        self.isCollide = False