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
        self.lastDirection = None
        self.listDirections = None
        self.listTextures = None
        self.direction = Turn.RIGHT
        self.buffer = Turn.NONE

        self.lives = 3
        self.animator = Animator()
        self.elapsedDist = 0
        self.matrixPosition = vec.Vector2(13, 23)

        self.destinationRectangle = None

        self.isBoosted = False
        self.isActive = True

        self.t = 0
        self.timeMove = 10
        self.timeBoost = 600


    def loadContent(self):
        path = os.getcwd() + "/Content/"

        move_right = pyray.load_texture(path + "PacmanMoveRight.png")
        move_left = pyray.load_texture(path + "PacmanMoveLeft.png")
        move_up = pyray.load_texture(path + "PacmanMoveUp.png")
        move_down = pyray.load_texture(path + "PacmanMoveDown.png")
        death = pyray.load_texture(path + "PacmanDeath.png")

        self.animator.addAnimation(move_right, 2, 0.5, True, "MoveRight")
        self.animator.addAnimation(move_left, 2, 0.5, True, "MoveLeft")
        self.animator.addAnimation(move_up, 2, 0.5, True, "MoveUp")
        self.animator.addAnimation(move_down, 2, 0.5, True, "MoveDown")

        self.listTextures = {
            "MoveRight": move_right,
            "MoveLeft": move_left,
            "MoveUp": move_up,
            "MoveDown": move_down,
            "Death": death
        }

        self.listDirections = {
            "MoveDown": vec.Vector2(0, 1),
            "MoveUp": vec.Vector2(0, -1),
            "MoveRight": vec.Vector2(1, 0),
            "MoveLeft": vec.Vector2(-1, 0),
            "None": vec.Vector2(0, 0)
        }

        self.destinationRectangle = pyray.Rectangle(self.matrixX() * 16 * 3 / 2 - 16 * 3 / 4,
                                                    self.matrixY() * 16 * 3 / 2 - 16 * 3 / 4 + AppCore.Managers.AppManager.upspace,
                                                    16 * 3, 16 * 3)

    def draw(self):
        name = None
        if self.isActive:
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

            vec_dir = self.listDirections[name]
            if self.direction == Turn.NONE:
                vec_dir = self.listDirections["None"]

            scale = GameManager().scale
            texture = self.listTextures[name]
            source_rectangle = self.animator.getSourceRectangle(name)

            width = source_rectangle.width
            height = source_rectangle.height

            self.destinationRectangle = pyray.Rectangle(self.matrixX() * width * scale / 2 - width * scale / 4 + self.elapsedDist * vec_dir.x,
                                                   self.matrixY() * height * scale / 2 - height * scale / 4 + self.elapsedDist * vec_dir.y + AppCore.Managers.AppManager.upspace,
                                                   width * scale, height * scale)

            pyray.draw_texture_pro(texture, source_rectangle, self.destinationRectangle, pyray.Vector2(0, 0), 0, pyray.WHITE)
            # pyray.draw_rectangle_lines_ex(destinationRectangle, 1, pyray.RED)

            self.elapsedDist += width * scale * (1/self.timeMove) / 2
        else:
            scale = GameManager().scale
            texture = self.listTextures["Death"]
            source_rectangle = self.animator.getSourceRectangle("Death")

            width = source_rectangle.width
            height = source_rectangle.height

            self.destinationRectangle = pyray.Rectangle(
                self.matrixX() * width * scale / 2 - width * scale / 4,
                self.matrixY() * height * scale / 2 - height * scale / 4 + AppCore.Managers.AppManager.upspace,
                width * scale, height * scale)

            pyray.draw_texture_pro(texture, source_rectangle, self.destinationRectangle, pyray.Vector2(0, 0), 0,
                                   pyray.WHITE)

    def Death(self):
        self.lives -= 1
        self.isActive = False
        self.direction = Turn.RIGHT
        self.buffer = Turn.NONE
        self.animator.addAnimation(self.listTextures["Death"], 11, 2, False, "Death")

    def FoodCollisionCheck(self):
        if GameManager().ReturnFood(self.matrixX(), self.matrixY()):
            GameManager().FoodCollision(self)

    def WallCollisionCheck(self):
        if self.direction != Turn.NONE:
            if self.direction == Turn.RIGHT and 27 > self.matrixX() > 0:
                if GameManager().ReturnObject(self.matrixX() + 1, self.matrixY()):
                    self.direction = Turn.NONE
            elif self.direction == Turn.LEFT and 0 < self.matrixX() < 27:
                if GameManager().ReturnObject(self.matrixX() - 1, self.matrixY()):
                    self.direction = Turn.NONE
            elif self.direction == Turn.UP:
                if GameManager().ReturnObject(self.matrixX(), self.matrixY() - 1):
                    self.direction = Turn.NONE
            elif self.direction == Turn.DOWN:
                if GameManager().ReturnObject(self.matrixX(), self.matrixY() + 1):
                    self.direction = Turn.NONE

    def move(self):
        if self.direction != Turn.NONE:
            if self.direction == Turn.RIGHT:
                    self.setmatrixX(self.matrixX() + 1)
                    if self.matrixX() > 27:
                        self.setmatrixX(0)
            elif self.direction == Turn.LEFT:
                    self.setmatrixX(self.matrixX() - 1)
                    if self.matrixX() < 0:
                        self.setmatrixX(27)
            elif self.direction == Turn.UP:
                    self.setmatrixY(self.matrixY() - 1)
            elif self.direction == Turn.DOWN:
                    self.setmatrixY(self.matrixY() + 1)

    def checkBuffer(self):
        if self.buffer != Turn.NONE:
            if self.buffer == Turn.RIGHT:
                if not GameManager().ReturnObject(self.matrixX() + 1, self.matrixY()):
                    self.turn(Turn.RIGHT)
            elif self.buffer == Turn.LEFT:
                if not GameManager().ReturnObject(self.matrixX() - 1, self.matrixY()):
                    self.turn(Turn.LEFT)
            elif self.buffer == Turn.UP:
                if not GameManager().ReturnObject(self.matrixX(), self.matrixY() - 1):
                    self.turn(Turn.UP)
            elif self.buffer == Turn.DOWN:
                if not GameManager().ReturnObject(self.matrixX(), self.matrixY() + 1):
                    self.turn(Turn.DOWN)

    def keyboardPressProcesser(self):
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_W):
                self.turn(Turn.UP)
        elif pyray.is_key_pressed(pyray.KeyboardKey.KEY_A):
            self.turn(Turn.LEFT)
        elif pyray.is_key_pressed(pyray.KeyboardKey.KEY_S):
            self.turn(Turn.DOWN)
        elif pyray.is_key_pressed(pyray.KeyboardKey.KEY_D):
            self.turn(Turn.RIGHT)

    def turn(self, new_direction):
            f = GameManager().return_time()
            if new_direction == Turn.RIGHT and 0 < self.matrixX() < 27:
                if GameManager().ReturnObject(self.matrixX() + 1, self.matrixY()) == False and f % self.timeMove == 0:
                    self.direction = Turn.RIGHT
                    self.buffer = Turn.NONE
                else:
                    self.buffer = Turn.RIGHT
            elif new_direction == Turn.LEFT and 0 < self.matrixX() < 27:
                if GameManager().ReturnObject(self.matrixX() - 1, self.matrixY()) == False and f % self.timeMove == 0:
                    self.direction = Turn.LEFT
                    self.buffer = Turn.NONE
                else:
                    self.buffer = Turn.LEFT
            elif new_direction == Turn.UP:
                if GameManager().ReturnObject(self.matrixX(), self.matrixY() - 1) == False and f % self.timeMove == 0:
                    self.direction = Turn.UP
                    self.buffer = Turn.NONE
                else:
                    self.buffer = Turn.UP
            elif new_direction == Turn.DOWN:
                if GameManager().ReturnObject(self.matrixX(), self.matrixY() + 1) == False and f % self.timeMove == 0:
                    self.direction = Turn.DOWN
                    self.buffer = Turn.NONE
                else:
                    self.buffer = Turn.DOWN

    def update(self):
        f = GameManager().return_time()
        if self.isActive:
            if f % self.timeMove == 0:
                self.move()
                self.checkBuffer()
                self.elapsedDist = 0
            if not self.direction == Turn.NONE:
                self.animator.updateRectangles()
            self.WallCollisionCheck()
            self.FoodCollisionCheck()
            self.keyboardPressProcesser()
            if self.isBoosted:
                self.t += 1
                if self.t % self.timeBoost == 0:
                    self.isBoosted = False
                    self.t = 0
        else:
            self.animator.updateRectangles()
            if len(self.animator.animations) == 4:
                if self.lives == 0:
                    AppCore.Managers.AppManager.instance.SwitchState('menu')
                    AppCore.Managers.AppManager.instance.GUIManager.reInit("you lost!", AppCore.Managers.AppManager.instance.GameManager.score)
                else:
                    self.isActive = True
                    self.reset()
                    GameManager().enableAllGhosts()
                    GameManager().resetTime()

    def reset(self):
        self.matrixPosition = vec.Vector2(13, 23)

class Ghost(GameObject, ITextureableObject):
    def __init__(self):
        super().__init__()
        self.destinationRectangle = None
        self.Frightened = False
        self.Timeout = False
        self.disable = False
        self.path = None

        self.elapsedDist = 0
        self.movAnimator = Animator()
        self.deathAnimator = Animator()
        self.listTextures = None
        self.dir = vec.Vector2(0, 0)
        self.gName = ""

        self.t = 0
        self.timeMove = 15
        self.timePath = 60
        self.timeLock = 200



    def loadContent(self):
        path = os.getcwd() + "/Content/"

        move_right = pyray.load_texture(path + f"Ghost{self.gName}MoveRight.png")
        move_left = pyray.load_texture(path + f"Ghost{self.gName}MoveLeft.png")
        move_up = pyray.load_texture(path + f"Ghost{self.gName}MoveUp.png")
        move_down = pyray.load_texture(path + f"Ghost{self.gName}MoveDown.png")

        self.movAnimator.addAnimation(move_right, 2, 0.5, True, "Right")
        self.movAnimator.addAnimation(move_left, 2, 0.5, True, "Left")
        self.movAnimator.addAnimation(move_up, 2, 0.5, True, "Up")
        self.movAnimator.addAnimation(move_down, 2, 0.5, True, "Down")

        self.listTextures = {
            "Right": move_right,
            "Left": move_left,
            "Up": move_up,
            "Down": move_down,
        }

        self.destinationRectangle = pyray.Rectangle(self.matrixX() * 16 * 3 / 2 - 16 * 3 / 4,
                                                    self.matrixY() * 16 * 3 / 2 - 16 * 3 / 4 + AppCore.Managers.AppManager.upspace,
                                                    16 * 3, 16 * 3)

    def draw(self):
        if not self.disable:
            name = "Right"
            if self.dir.x == 1:
                name = "Right"
            elif self.dir.x == -1:
                name = "Left"
            elif self.dir.y == -1:
                name = "Up"
            elif self.dir.y == 1:
                name = "Down"

            if self.Timeout:
                self.dir = vec.Vector2(0, 0)

            scale = GameManager().scale
            texture = self.listTextures[name]

            source_rectangle = self.movAnimator.getSourceRectangle(name)

            width = source_rectangle.width
            height = source_rectangle.height

            self.destinationRectangle = pyray.Rectangle(
                (self.matrixX() - self.dir.x) * width * scale / 2 - width * scale / 4 + self.elapsedDist * self.dir.x,
                (self.matrixY() - self.dir.y) * height * scale / 2 - height * scale / 4 + self.elapsedDist * self.dir.y + AppCore.Managers.AppManager.upspace,
                width * scale, height * scale)

            pyray.draw_texture_pro(texture, source_rectangle, self.destinationRectangle, pyray.Vector2(0, 0), 0, pyray.WHITE)

            if not self.disable:
                self.elapsedDist += width * scale * (1 / self.timeMove) / 2
        # pyray.draw_rectangle_lines_ex(self.destinationRectangle, 1, pyray.RED)

    def Death(self):
        self.Frightened = False
        self.Timeout = True
        self.path = None
        self.reset()

    def move(self):
        if self.path is not None:
            if len(self.path) != 0:
                self.dir = self.path[-1]

                self.matrixPosition = vec.Vector2(self.path[-1].x + self.matrixX(), self.matrixY())
                self.matrixPosition = vec.Vector2(self.matrixX(), self.matrixY() + self.path[-1].y)

                self.path.pop()

        if self.matrixX() < 0:
            self.matrixPosition = vec.Vector2(27, self.matrixY())
        elif self.matrixX() > 27:
            self.matrixPosition = vec.Vector2(0, self.matrixY())

    def getPath(self):
        pass

    def reset(self):
        self.destinationRectangle = pyray.Rectangle(self.matrixX() * 16 * 3 / 2 - 16 * 3 / 4,
                                                    self.matrixY() * 16 * 3 / 2 - 16 * 3 / 4 + AppCore.Managers.AppManager.upspace,
                                                    16 * 3, 16 * 3)
        self.Timeout = True
        self.t = 0

    def spawn(self):
        self.matrixPosition = vec.Vector2(13, 11)

    def update(self):
        time = GameManager().return_time()

        if not self.disable:
            self.movAnimator.updateRectangles()
            if not self.Timeout:
                if time % self.timePath == 0:
                    self.getPath()
                if time % self.timeMove == 0:
                    self.move()
                    self.elapsedDist = 0
            else:
                if self.t // self.timeLock == 1:
                    self.Timeout = False
                    self.spawn()
                self.t += 1


class RedGhost(Ghost):
    def __init__(self):
        super().__init__()
        self.gName = "Red"

    def reset(self):
        self.matrixPosition = vec.Vector2(12, 14)
        super().reset()

    def getPath(self):
        self.path = GameManager().findShortestPath(self.matrixPosition, GameManager().getPlayerPos())
        print(len(self.path))
        super().getPath()

class PinkGhost(Ghost):
    def __init__(self):
        super().__init__()
        self.gName = "Pink"
        self.timePath = 30
        self.timeLock = 400

    def reset(self):
        self.matrixPosition = vec.Vector2(15, 14)
        super().reset()

    def getPath(self):
        pos=GameManager().getPlayerPos()

        if GameManager().getPlayerDirection()==Turn.RIGHT:
            if pos.x <= 22:
                for i in range(1, 5, -1):
                    if not GameManager().ReturnObject(pos.x + i, pos.y):
                        self.path = GameManager().findShortestPath(self.matrixPosition, vec.Vector2(pos.x + i, pos.y - i))
                        return
            self.path = GameManager().findShortestPath(self.matrixPosition, GameManager().getPlayerPos())

        if GameManager().getPlayerDirection() == Turn.LEFT:
            if pos.x >= 5:
                for i in range(1, 5, -1):
                    if not GameManager().ReturnObject(pos.x - i, pos.y):
                        self.path = GameManager().findShortestPath(self.matrixPosition, vec.Vector2(pos.x - i, pos.y - i))
                        return
            self.path = GameManager().findShortestPath(self.matrixPosition, GameManager().getPlayerPos())

        if GameManager().getPlayerDirection() == Turn.UP:
            if pos.y >= 5:
                for i in range(1, 5, -1):
                    if not GameManager().ReturnObject(pos.x , pos.y - i):
                        self.path = GameManager().findShortestPath(self.matrixPosition, vec.Vector2(pos.x - i, pos.y - i))
                        return
            self.path = GameManager().findShortestPath(self.matrixPosition, GameManager().getPlayerPos())

        if GameManager().getPlayerDirection() == Turn.DOWN:
            if pos.y <= 25:
                for i in range(1, 5, -1):
                    if not GameManager().ReturnObject(pos.x, pos.y + i):
                        self.path = GameManager().findShortestPath(self.matrixPosition, vec.Vector2(pos.x + i, pos.y + i))
                        return
            self.path = GameManager().findShortestPath(self.matrixPosition, GameManager().getPlayerPos())

        super().getPath()

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

    def onCollision(self):
        if self.active:
            GameManager().boost_player()
            GameManager().FrightAllGhosts()
            self.active = False

    def draw(self):
        if self.active:
            pyray.draw_texture_ex(self.texture, pyray.Vector2(self.X, self.Y), 0, 3.0, pyray.WHITE)
