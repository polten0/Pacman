from ObjectClasses.Objects import MapObject
import os

class Wall(MapObject):
    def __init__(self):
        super().__init__()
        self.isCollide = True
        self.filepath = f"{os.getcwd()}/Content/Maps/Wall.png"

class Floor(MapObject):
    def __init__(self):
        super().__init__()
        self.isCollide = False