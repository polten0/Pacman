from AppCore.Managers import GameManager
from Objects import GameObject


class Turn:
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    NONE = 0

class Player(GameObject):
    def __init__(self):
        self.speed = 5
        self.turn = Turn.RIGHT
        self.buffer = Turn.NONE
    def onCollision(self, collide_object):
        if (isinstance(collide_object, Food)):
            collide_object.onCollision(self)
        elif (isinstance(collide_object, Ghost)):
            if (GameManager.player_is_boosted == False):
                self.Death()
            if (GameManager.player_is_boosted):
                collide_object.onCollision(self)
        elif (isinstance(collide_object, BigFood)):
            collide_object.onCollision()
            GameManager.boost_player()
        elif (isinstance(collide_object, Wall)):
            pass

    def Death(self):
        pass

    def move(self):
        if (isinstance(self.turn, Turn.NONE) == False):
            if (isinstance(self.turn, Turn.RIGHT)):
                self.vectorPosition.x += self.speed
            elif (isinstance(self.turn, Turn.LEFT)):
                self.vectorPosition.x -= self.speed
            elif (isinstance(self.turn, Turn.UP)):
                self.vectorPosition.y -= self.speed
            elif (isinstance(self.turn, Turn.DOWN)):
                self.vectorPosition.y += self.speed

    def checkBuffer(self):
        if (isinstance(self.buffer, Turn.NONE) == False):
            if (isinstance(self.buffer, Turn.RIGHT)):
                pass
            elif (isinstance(self.buffer, Turn.LEFT)):
                pass
            elif (isinstance(self.buffer, Turn.UP)):
                pass
            elif (isinstance(self.buffer, Turn.DOWN)):
                pass

    def turn(self):
        pass



    # вот тут пропишите, функции должны возвращать позиции в массиве по X и по Y
    def getPositionX(self):
        pass
    def getPositionY(self):
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
            GameManager.addScore(self)
            self.active = False

class BigFood(Food):
    def __init__(self):
        super().__init__()



