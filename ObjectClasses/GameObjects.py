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
        if (self.direction != Turn.NONE):
            f = GameManager().return_time() % 30
            if f <= 30:
                if (self.direction == Turn.RIGHT):
                        GameManager().pacman_position.x += 1
                elif (self.direction == Turn.LEFT):
                        GameManager().pacman_position.x -= 1
                elif (self.direction == Turn.UP):
                        GameManager().pacman_position.y -= 1
                elif (self.direction == Turn.DOWN):
                        GameManager().pacman_position.y += 1
            if (f == 30):
                self.checkBuffer()

    def checkBuffer(self):
        if (self.direction == Turn.NONE):
            if (self.direction == Turn.RIGHT):
                if (GameManager().ReturnObject(GameManager().pacman_position.x + 1, GameManager().pacman_position.y) == False):
                    self.turn(Turn.RIGHT)
                else:
                    self.onCollision(Wall)
            elif (self.direction == Turn.LEFT):
                if (GameManager().ReturnObject(GameManager().pacman_position.x - 1, GameManager().pacman_position.y) == False):
                    self.turn(Turn.LEFT)
                else:
                    self.onCollision(Wall)
            elif (self.direction == Turn.UP):
                if (GameManager().ReturnObject(GameManager().pacman_position.x, GameManager().pacman_position.y - 1) == False):
                    self.turn(Turn.UP)
                else:
                    self.onCollision(Wall)
            elif (self.direction == Turn.DOWN):
                if (GameManager().ReturnObject(GameManager().pacman_position.x, GameManager().pacman_position.y + 1) == False):
                    self.turn(Turn.DOWN)
                else:
                    self.onCollision(Wall)
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
                if (GameManager().ReturnObject(GameManager().pacman_position.x + 1, GameManager().pacman_position.y) == False):
                    self.direction = Turn.RIGHT
                else:
                    self.buffer = Turn.RIGHT
            elif (new_direction == Turn.LEFT):
                if (GameManager().ReturnObject(GameManager().pacman_position.x - 1, GameManager().pacman_position.y) == False):
                    self.direction = Turn.LEFT
                else:
                    self.buffer = Turn.LEFT
            elif (new_direction == Turn.UP):
                if (GameManager().ReturnObject(GameManager().pacman_position.x, GameManager().pacman_position.y - 1) == False):
                    self.direction = Turn.UP
                else:
                    self.buffer = Turn.UP
            elif (new_direction == Turn.DOWN):
                if (GameManager().ReturnObject(GameManager().pacman_position.x, GameManager().pacman_position.y + 1) == False):
                    self.direction = Turn.DOWN
                else:
                    self.buffer = Turn.DOWN


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



