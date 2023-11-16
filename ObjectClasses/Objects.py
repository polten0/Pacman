import pyray

from AppCore.Interfaces import Interfaces
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

class MapObject(Object, Interfaces.IDrawableObject):
    def __init__(self):
        super().__init__()

    def draw(self):
        pass

class UIObject(Object, Interfaces.IUpdateableObject,
                 Interfaces.IDrawableObject):
    def __init__(self):
        super().__init__()

    def draw(self):
        pass

    def update(self):
        pass
