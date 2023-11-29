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
        self.matrixPosition = vec.Vector2(x=1, y=1)

    def draw(self):
        pass

    def update(self):
        pass

    def loadContent(self):
        pass

    def onCollison(self):
        pass

    def rec(self):
        pass

    def matrixY(self):
        return self.matrixPosition.y

    def matrixX(self):
        return self.matrixPosition.x


    def setmatrixX(self, new):
        self.matrixPosition = vec.Vector2(new, self.matrixPosition.y)

    def setmatrixY(self, new):
        self.matrixPosition = vec.Vector2(self.matrixPosition.x, new)

class MapObject(Object, Interfaces.IDrawableObject, Interfaces.ITextureableObject):
    def __init__(self):
        super().__init__()
        self.width = 8
        self.height = 8
        self.filepath = ""
        self.scale = 3.0

        self.imageX = 0
        self.imageY = 0

        self.X = 0
        self.Y = 0

        self.collisionRectangle = None
        self.sourceRectangle = None

        self.texture = None
        self.isCollide = None

    def loadContent(self):
        self.texture = pyray.load_texture(self.filepath)

        self.sourceRectangle = pyray.Rectangle(self.imageX, self.imageY, self.width, self.height)
        self.collisionRectangle = pyray.Rectangle(self.X, self.Y, self.width * self.scale, self.height * self.scale)

    def draw(self):
        pyray.draw_texture_pro(self.texture, self.sourceRectangle, self.collisionRectangle,
                               pyray.Vector2(0, 0), 0, pyray.WHITE)
        # pyray.draw_rectangle_lines_ex(self.collisionRectangle, 0.5, pyray.GREEN)



class UIObject(Object, Interfaces.IUpdateableObject,
               Interfaces.IDrawableObject):
    def __init__(self):
        super().__init__()

    def draw(self):
        pass

    def update(self):
        pass

