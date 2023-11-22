import pyray

from AppCore import Interfaces
import vec

class Object:
    def __init__(self):
        self.vectorPosition = vec.Vector2(x=0, y=0)

    @property
    def X(self):
        return self.vectorPosition.x

    @X.setter
    def X(self, new):
        self.vectorPosition = vec.Vector2(new, self.vectorPosition.y)

    @property
    def Y(self):
        return self.vectorPosition.y

    @Y.setter
    def Y(self, new):
        self.vectorPosition = vec.Vector2(self.vectorPosition.x, new)

class GameObject(Object, Interfaces.IUpdateableObject,
                 Interfaces.IDrawableObject):
    def __init__(self):
        super().__init__()

    def draw(self):
        pass

    def update(self):
        pass

    def onCollison(self):
        pass

class MapObject(Object, Interfaces.IDrawableObject, Interfaces.ITextureableObject):
    def __init__(self):
        super().__init__()
        self.size = 16
        self.filepath = ""

        self.texture = None

    def loadContent(self):
        self.texture = pyray.load_texture(self.filepath)

    def draw(self):
        pyray.draw_texture(self.texture, self.X, self.Y, pyray.WHITE)

class UIObject(Object, Interfaces.IUpdateableObject,
               Interfaces.IDrawableObject):
    def __init__(self):
        super().__init__()

    def draw(self):
        pass

    def update(self):
        pass
