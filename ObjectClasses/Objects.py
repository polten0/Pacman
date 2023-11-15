from AppCore.Interfaces import Interfaces
import vec


class GameObject(Interfaces.IUpdateableObject,
                 Interfaces.IDrawableObject):
    def __init__(self):
        self.vectorPosition = vec.Vector2(x=0, y=0)

    @property
    def X(self):
        return self.vectorPosition.x
    @X.setter
    def X(self, new):
        self.vectorPosition.x = new

    @property
    def Y(self):
        return self.vectorPosition.y
    @Y.setter
    def Y(self, new):
        self.vectorPosition.y = new

    def draw(self):
        pass

    def update(self):
        pass

class MapObject(Interfaces.IDrawableObject):
    def __init__(self):
        self.vectorPosition = vec.Vector2(x=0, y=0)

    @property
    def X(self):
        return self.vectorPosition.x
    @X.setter
    def X(self, new):
        self.vectorPosition.x = new

    @property
    def Y(self):
        return self.vectorPosition.y
    @Y.setter
    def Y(self, new):
        self.vectorPosition.y = new

    def draw(self):
        pass