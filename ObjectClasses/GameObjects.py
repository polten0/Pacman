import pyray

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
    return AppCore.Managers.AppManager.instance.gameManager

class Player(GameObject):
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.direction = Turn.RIGHT
        self.buffer = Turn.NONE

    def draw(self):
        pyray.draw_rectangle(self.matrixPosition.x * 8 * GameManager().scale, self.matrixPosition.y * 8 * GameManager().scale, 8 * GameManager().scale, 8 * GameManager().scale, pyray.YELLOW)

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

    def WallCollisionCheck(self):
        if (self.direction != Turn.NONE):
            if (self.direction == Turn.RIGHT):
                if (GameManager().ReturnObject(self.matrixX() + 1, self.matrixY()) == True):
                    self.direction = Turn.NONE
            elif (self.direction == Turn.LEFT):
                if (GameManager().ReturnObject(self.matrixX() - 1, self.matrixY()) == True):
                    self.direction = Turn.NONE
            elif (self.direction == Turn.UP):
                if (GameManager().ReturnObject(self.matrixX(), self.matrixY() - 1) == True):
                    self.direction = Turn.NONE
            elif (self.direction == Turn.DOWN):
                if (GameManager().ReturnObject(self.matrixX(), self.matrixY() + 1) == True):
                    self.direction = Turn.NONE

    def Death(self):
        pass

    def move(self):
        if (self.direction != Turn.NONE):
            if (self.direction == Turn.RIGHT):
                    self.setmatrixX(self.matrixX() + self.speed)
                    if (self.matrixX() > 26):
                        self.setmatrixX(0)
            elif (self.direction == Turn.LEFT):
                    self.setmatrixX(self.matrixX() - self.speed)
                    if (self.matrixX() == 0):
                        self.setmatrixX(27)
            elif (self.direction == Turn.UP):
                    self.setmatrixY(self.matrixY() - self.speed)
            elif (self.direction == Turn.DOWN):
                    self.setmatrixY(self.matrixY() + self.speed)

    def checkBuffer(self):
        if (self.buffer != Turn.NONE):
            if (self.buffer == Turn.RIGHT):
                if (GameManager().ReturnObject(self.matrixX() + 1, self.matrixY()) == False):
                    self.turn(Turn.RIGHT)
            elif (self.buffer == Turn.LEFT):
                if (GameManager().ReturnObject(self.matrixX() - 1, self.matrixY()) == False):
                    self.turn(Turn.LEFT)
            elif (self.buffer == Turn.UP):
                if (GameManager().ReturnObject(self.matrixX(), self.matrixY() - 1) == False):
                    self.turn(Turn.UP)
            elif (self.buffer == Turn.DOWN):
                if (GameManager().ReturnObject(self.matrixX(), self.matrixY() + 1) == False):
                    self.turn(Turn.DOWN)
    def keyboardPressProcesser(self):
        if (pyray.is_key_pressed(pyray.KeyboardKey.KEY_W)):
            self.turn(Turn.UP)
        elif (pyray.is_key_pressed(pyray.KeyboardKey.KEY_A)):
            self.turn(Turn.LEFT)
        elif (pyray.is_key_pressed(pyray.KeyboardKey.KEY_S)):
            self.turn(Turn.DOWN)
        elif (pyray.is_key_pressed(pyray.KeyboardKey.KEY_D)):
            self.turn(Turn.RIGHT)

    def turn(self, new_direction):
            if (new_direction == Turn.RIGHT):
                if (GameManager().ReturnObject(self.matrixX() + 1, self.matrixY()) == False):
                    self.direction = Turn.RIGHT
                    self.buffer = Turn.NONE
                else:
                    self.buffer = Turn.RIGHT
            elif (new_direction == Turn.LEFT):
                if (GameManager().ReturnObject(self.matrixX() - 1, self.matrixY()) == False):
                    self.direction = Turn.LEFT
                    self.buffer = Turn.NONE
                else:
                    self.buffer = Turn.LEFT
            elif (new_direction == Turn.UP):
                if (GameManager().ReturnObject(self.matrixX(), self.matrixY() - 1) == False):
                    self.direction = Turn.UP
                    self.buffer = Turn.NONE
                else:
                    self.buffer = Turn.UP
            elif (new_direction == Turn.DOWN):
                if (GameManager().ReturnObject(self.matrixX(), self.matrixY() + 1) == False):
                    self.direction = Turn.DOWN
                    self.buffer = Turn.NONE
                else:
                    self.buffer = Turn.DOWN


    def update(self):
        f = GameManager().return_time() % 60
        self.WallCollisionCheck()
        self.keyboardPressProcesser()
        self.checkBuffer()
        print(self.buffer)
        if (f % 2 == 0):
            self.move()

        f += 1

        if (f == 60):
            f = 0




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



