import os

import pyray
import vec
import AppCore.Managers
from ObjectClasses.Objects import GameObject
from AppCore.Animator import Animator
from AppCore.Interfaces import ITextureableObject


class Turn:
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    NONE = 0

def GameManager():
    return AppCore.Managers.AppManager.instance.gameManager

class Player(GameObject, ITextureableObject):
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.direction = Turn.RIGHT
        self.buffer = Turn.NONE
        self.timeMove = 20

        self.animator = Animator()
        self.elapsedDist = 0

    def loadContent(self):
        path = os.getcwd() + "/Content/"

        moveRight = pyray.load_texture(path + "PacmanMoveRight.png")
        moveLeft = pyray.load_texture(path + "PacmanMoveLeft.png")
        moveUp = pyray.load_texture(path + "PacmanMoveUp.png")
        moveDown = pyray.load_texture(path + "PacmanMoveDown.png")

        self.animator.addAnimation(moveRight, 2, 0.5, True, "MoveRight")
        self.animator.addAnimation(moveLeft, 2, 0.5, True, "MoveLeft")
        self.animator.addAnimation(moveUp, 2, 0.5, True, "MoveUp")
        self.animator.addAnimation(moveDown, 2, 0.5, True, "MoveDown")

        self.listTextures = {
            "MoveRight": moveRight,
            "MoveLeft": moveLeft,
            "MoveUp": moveUp,
            "MoveDown": moveDown,
        }

        self.listDirections = {
            "MoveDown": vec.Vector2(0, 1),
            "MoveUp": vec.Vector2(0, -1),
            "MoveRight": vec.Vector2(1, 0),
            "MoveLeft": vec.Vector2(-1, 0),
            "None": vec.Vector2(0, 0)
        }

    def draw(self):
        if self.direction == Turn.RIGHT:
            name = "MoveRight"
            self.lastDirection = name
        elif self.direction == Turn.LEFT:
            name = "MoveLeft"
            self.lastDirection = name
        elif self.direction == Turn.UP:
            name = "MoveUp"
            self.lastDirection = name
        elif self.direction == Turn.DOWN:
            name = "MoveDown"
            self.lastDirection = name
        elif self.direction == Turn.NONE:
            name = self.lastDirection

        vecDir = self.listDirections[name]
        if self.direction == Turn.NONE:
            vecDir = self.listDirections["None"]

        scale = GameManager().scale
        texture = self.listTextures[name]
        sourceRectangle = self.animator.getSourceRectangle(name)

        width = sourceRectangle.width
        height = sourceRectangle.height
        t = GameManager().return_time()

        destinationRectangle = pyray.Rectangle(self.matrixX() * width * scale / 2 - width * scale / 4 + self.elapsedDist * vecDir.x,
                                               self.matrixY() * height * scale / 2 - height * scale / 4 + self.elapsedDist * vecDir.y + AppCore.Managers.AppManager.upspace,
                                               width * scale, height * scale)

        pyray.draw_texture_pro(texture, sourceRectangle, destinationRectangle, pyray.Vector2(0, 0), 0, pyray.WHITE)
        # pyray.draw_rectangle_lines_ex(destinationRectangle, 1, pyray.RED)

        self.elapsedDist += width * scale * (1/self.timeMove) / 2



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


    def FoodCollisionCheck(self):
        if (GameManager().ReturnFood(self.matrixX(), self.matrixY()) == True):
            GameManager().FoodCollision(self)


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
        f = GameManager().return_time()

        if not self.direction == Turn.NONE:
            self.animator.updateRectangles()
        self.WallCollisionCheck()
        self.FoodCollisionCheck()
        self.keyboardPressProcesser()
        self.checkBuffer()

        if (f % self.timeMove == 0):
            self.move()
            self.elapsedDist = 0




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

class Food(GameObject, ITextureableObject):
    def __init__(self):
        super().__init__()
        self.active = True
        self.texture = None

    def loadContent(self):
        self.texture = pyray.load_texture(f'{os.getcwd()}/Content/Food.png')

    def onCollision(self):
        if self.active:
            GameManager().addScore(self)
            self.active = False

    def draw(self):
        if self.active:
            pyray.draw_texture_ex(self.texture, pyray.Vector2(self.X, self.Y), 0, GameManager().scale, pyray.WHITE)

class BigFood(Food):
    def __init__(self):
        super().__init__()
        self.active = True
        self.texture = None

    def loadContent(self):
        self.texture = pyray.load_texture(f'{os.getcwd()}/Content/BigFood.png')

    def draw(self):
        if self.active:
            pyray.draw_texture_ex(self.texture, pyray.Vector2(self.X, self.Y), 0, 3.0, pyray.WHITE)
