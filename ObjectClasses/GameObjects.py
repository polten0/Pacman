import AppCore.Managers
from ObjectClasses.Objects import GameObject
from ObjectClasses.MapObjects import Wall


class Turn:
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    NONE = 0

def GameManager():
    return AppCore.Managers.AppManager.GameManager

class Player(GameObject):
    def __init__(self):
        self.speed = 5
        self.direction = Turn.RIGHT
        self.buffer = Turn.NONE

    def onCollision(self, collide_object):
        if (isinstance(collide_object, Food)):
            collide_object.onCollision(self)
        elif (isinstance(collide_object, Ghost)):
            if (GameManager().player_is_boosted == False):
                self.Death()
            if (GameManager().player_is_boosted):
                collide_object.onCollision(self)
        elif (isinstance(collide_object, BigFood)):
            collide_object.onCollision()
            GameManager().boost_player()
        elif (isinstance(collide_object, Wall)):
            pass

    def Death(self):
        pass

    def move(self):
        if (isinstance(self.direction, Turn.NONE) == False):
            if (isinstance(self.direction, Turn.RIGHT)):
                self.vectorPosition.x += self.speed
            elif (isinstance(self.direction, Turn.LEFT)):
                self.vectorPosition.x -= self.speed
            elif (isinstance(self.direction, Turn.UP)):
                self.vectorPosition.y -= self.speed
            elif (isinstance(self.direction, Turn.DOWN)):
                self.vectorPosition.y += self.speed

    def checkBuffer(self):
        if (isinstance(self.buffer, Turn.NONE) == False):
            if (isinstance(self.buffer, Turn.RIGHT)):
                if (GameManager().ReturnObject(self.X + 1, self.Y) == False):
                    self.turn(Turn.RIGHT)
                else:
                    pass
            elif (isinstance(self.buffer, Turn.LEFT)):
                if (GameManager().ReturnObject(self.X - 1, self.Y) == False):
                    self.turn(Turn.LEFT)
                else:
                    pass
            elif (isinstance(self.buffer, Turn.UP)):
                if (GameManager().ReturnObject(self.X, self.Y - 1) == False):
                    self.turn(Turn.UP)
                else:
                    pass
            elif (isinstance(self.buffer, Turn.DOWN)):
                if (GameManager().ReturnObject(self.X, self.Y + 1) == False):
                    self.turn(Turn.DOWN)
                else:
                    pass

    def turn(self):
        pass

class Ghost(GameObject):
    def __init__(self):
        self.Frightened = False
        self.Timeout = False

    def onCollision(self, collide_object):
        if (isinstance(collide_object, Player)):
            if (self.Frightened):
                self.Death()
            else:
                collide_object.onCollision()

    def Death(self):
        self.Frightened = False
        self.Timeout = True
        pass



class Food(GameObject):
    def __init__(self):
        self.active = True

    def onCollision(self):
        if (self.active):
            GameManager().addScore(self)
            self.active = False

class BigFood(Food):
    def __init__(self):
        super().__init__()



