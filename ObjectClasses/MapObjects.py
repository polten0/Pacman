from ObjectClasses.Objects import MapObject
from AppCore.Interfaces import ITextureableObject
import pyray
import os
class Wall(MapObject, ITextureableObject):
    def __init__(self):
        self.texture = None
        self.filepath = f"{os.getcwd()}/Content/BigFood.png"

    def loadContent(self):
        self.texture = pyray.load_texture(self.filepath)

    def draw(self):
        pyray.draw_texture(self.texture, 10, 10, pyray.WHITE)
