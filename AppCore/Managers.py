import pyray
import vec

from ObjectClasses.GameObjects import Player, Food, BigFood, RedGhost,PinkGhost
from ObjectClasses.Objects import GameObject
from ObjectClasses.MapObjects import Wall, Floor
from ObjectClasses.UIObjects import Label, Button
import json
import os


class AppManager:
    instance = None
    screenWidth = 673
    screenHeight = 950

    upspace = 100

    @property
    def GameManager(self):
        return self.gameManager

    def __init__(self):
        self.gameManager = GameManager()
        self.GUIManager = GUIManager()
        self.state = "menu"
        AppManager.instance = self

    def Initialization(self):
        pyray.init_window(AppManager.screenWidth, AppManager.screenHeight, 'Game')
        self.GUIManager.LoadContent()

    def SwitchState(self, state):
        if (state == "game"):
            self.gameManager = GameManager()
            self.gameManager.LoadContent()
        elif (state == "menu"):
            self.GUIManager.LoadContent()
        self.state = state


    def Update(self):
        if (self.state == "menu"):
            self.GUIManager.Update()
        if (self.state == "game"):
            self.gameManager.Update()

    def Draw(self):
        pyray.clear_background(pyray.BLACK)
        pyray.begin_drawing()

        if (self.state == "game"):
            self.gameManager.Draw()

        elif (self.state == "menu"):
            self.GUIManager.Draw()

        pyray.end_drawing()

class MapManager:
    def __init__(self):
        self.listMapObjects = list()
        self.listFoodObjects = list()
        self.matrixFood = None # Матрица еды. Наполнен GameObject, Food, BigFood
        self.matrix = None

    def loadContent(self):
        self.loadMap()
        for mapObject in self.listMapObjects:
            mapObject.loadContent()

        for food in self.listFoodObjects:
            food.loadContent()



    def Draw(self):
        for mapObject in self.listMapObjects:
            mapObject.draw()

        for food in self.listFoodObjects:
            food.draw()

    def loadMap(self):
        fullpath = f"{os.getcwd()}/Content/Maps/"

        map = open(fullpath + "Map1.json").read()
        mapdict = json.loads(map)

        layer = mapdict["layers"][0]

        tilesetpath = mapdict["tilesets"][0]["source"]
        tileset = json.loads(open(fullpath + tilesetpath).read())

        tileHeight = tileset["tileheight"]
        tileWidth = tileset["tilewidth"]
        spacing = tileset["spacing"]
        columns = tileset["columns"]
        imagePath = tileset["image"]

        tiles = tileset["tiles"]
        data = layer["data"]
        dataFood = mapdict["layers"][1]["data"]
        dataSizeRows = layer["height"]
        dataSizeColumns = layer["width"]

        self.matrix = [[0 for j in range(dataSizeColumns)] for i in range(dataSizeRows)]
        self.matrixFood = [[0 for j in range(dataSizeColumns)] for i in range(dataSizeRows)]

        c = 0
        for i in range(dataSizeRows):
            for e in range(dataSizeColumns):
                mapObject = None
                food = GameObject()
                foodGID = dataFood[c] - 1
                GID = data[c] - 1

                for tile in tiles:
                    if tile["id"] == GID:
                        if tile["type"] == "Wall":
                            mapObject = Wall()
                        elif tile["type"] == "Floor":
                            mapObject = Floor()
                    if tile["id"] == foodGID:
                        if tile["type"] == "Food":
                            food = Food()
                        elif tile["type"] == "BigFood":
                            food = BigFood()


                mapObject.width = tileWidth
                mapObject.height = tileHeight

                mapObject.imageX = tileWidth * (GID % columns) + spacing * (GID % columns)
                mapObject.imageY = tileHeight * (GID // columns) + spacing * (GID // columns)

                mapObject.X = e * tileWidth * mapObject.scale
                mapObject.Y = i * tileHeight * mapObject.scale + AppManager.upspace

                mapObject.filepath = fullpath + imagePath

                self.matrix[i][e] = mapObject
                self.listMapObjects.append(mapObject)

                food.X = mapObject.X
                food.Y = mapObject.Y

                self.matrixFood[i][e] = food
                self.listFoodObjects.append(food)

                c += 1

class GameManager:
    def __init__(self):
        self.score = 0
        self.mapManager = MapManager()
        self.Pacman = Player()
        self.scale = 3
        self.t = 0

        self.score_text = Label(10, 10, "SCORE:")
        self.score_label = Label(220, 10, str(self.score))
        self.lives_text = Label(10, 900, "LIVES:")
        self.lives_label = Label(220, 900, str(self.Pacman.lives))
        self.boosted_text = Label(430, 900, "boosted!")

        self.ghosts = []

        ghost = RedGhost()
        ghost.reset()
        self.ghosts.append(ghost)

        ghost = PinkGhost()
        ghost.reset()
        self.ghosts.append(ghost)


    def LoadContent(self):
        self.score = 0
        self.Pacman = Player()
        self.mapManager.loadContent()
        self.Pacman.loadContent()
        self.score_text.loadFont()
        self.score_label.loadFont()
        self.lives_text.loadFont()
        self.lives_label.loadFont()
        self.boosted_text.loadFont()
        for ghost in self.ghosts:
            ghost.loadContent()

    def Draw(self):
        self.score_text.draw()
        self.score_label.draw()
        self.lives_text.draw()
        self.lives_label.draw()
        self.mapManager.Draw()
        for ghost in self.ghosts:
            ghost.draw()
        self.Pacman.draw()
        if (self.Pacman.isBoosted):
            self.boosted_text.draw()


    def CheckAllFood(self):
        j = True
        for gameObjects in self.mapManager.matrixFood:
            for obj in gameObjects:
                if isinstance(obj, Food):
                    if obj.active:
                        j = False
        if (j):
            AppManager.instance.SwitchState("menu")
            AppManager.instance.GUIManager.reInit("you won!")

    def disableAllGhosts(self):
        for i in self.ghosts:
            i.disable = True

    def enableAllGhosts(self):
        for i in self.ghosts:
            i.disable = False

    def FrightAllGhosts(self):
        for i in self.ghosts:
            i.Frightened = True

    def deFrightAllGhosts(self):
        for i in self.ghosts:
            i.Frightened = False

    def resetGhosts(self):
        for ghost in self.ghosts:
            ghost.reset()

    def resetTime(self):
        t = 0



    def Update(self):
        self.t += 1
        self.Pacman.update()
        for ghost in self.ghosts:
            ghost.update()
            if pyray.check_collision_recs(ghost.destinationRectangle, self.Pacman.destinationRectangle):
                if self.Pacman.isBoosted:
                    ghost.Death()
                else:
                    if self.Pacman.isActive:
                        self.Pacman.Death()
                        self.disableAllGhosts()
                        self.resetGhosts()

        self.score_label.update(str(self.score))
        self.lives_label.update(str(self.Pacman.lives))
        self.CheckAllFood()


    def ReturnObject(self, x, y):
        return self.mapManager.matrix[y][x].isCollide

    def ReturnFood(self, x, y):
        if(isinstance(self.mapManager.matrixFood[y][x], Food)):
            return self.mapManager.matrixFood[y][x].active

    def FoodCollision(self, PlayerObject):
        self.mapManager.matrixFood[PlayerObject.matrixY()][PlayerObject.matrixX()].onCollision()

    def boost_player(self):
        self.Pacman.isBoosted = True

    def gameOver(self):
        pass

    def addScore(self, scoreObject):
        if (isinstance(scoreObject, Food)):
            self.score += 10
        if (isinstance(scoreObject, BigFood)):
            self.score += 50

    def getPlayerPos(self):
        return self.Pacman.matrixPosition

    def getPlayerDirection(self):
        return self.Pacman.direction

    def findShortestPath(self, matrixStart, matrixEnd):
        width = len(self.mapManager.matrix[0])
        height = len(self.mapManager.matrix)
        matrix = [[None for e in range(width)] for i in range(height)]
        path = []

        for i in range(height):
            for e in range(width):
                if isinstance(self.mapManager.matrix[i][e], Wall):
                    matrix[i][e] = -1

        matrix[matrixStart.y][matrixStart.x] = 0

        self.checkAndMark(matrix, matrixStart)
        self.buildPath(matrix, path, matrixEnd, matrixStart)

        # path.reverse()
        return path

    def checkAndMark(self, matrix, pos):
        """
        if matrixPosition.x == 0:
            if matrix[matrixPosition.y][matrixPosition.x + 1] == 0:
                matrix[matrixPosition.y][matrixPosition.x + 1] += matrix[matrixPosition.y][matrixPosition.x] + 1
        elif matrixPosition.x == len(matrix[0]):
            if matrix[matrixPosition.y][matrixPosition.x - 1] == 0:
                matrix[matrixPosition.y][matrixPosition.x - 1] += matrix[matrixPosition.y][matrixPosition.x] + 1
        else:
            if matrix[matrixPosition.y][matrixPosition.x - 1] == 0:
                matrix[matrixPosition.y][matrixPosition.x - 1] += matrix[matrixPosition.y][matrixPosition.x] + 1
            if matrix[matrixPosition.y][matrixPosition.x + 1] == 0:
                matrix[matrixPosition.y][matrixPosition.x + 1] += matrix[matrixPosition.y][matrixPosition.x] + 1


        if matrixPosition.y == 0:
            if matrix[matrixPosition.y + 1][matrixPosition.x] == 0:
                matrix[matrixPosition.y + 1][matrixPosition.x] += matrix[matrixPosition.y][matrixPosition.x] + 1
        elif matrixPosition.y == len(matrix[0]):
            if matrix[matrixPosition.y - 1][matrixPosition.x] == 0:
                matrix[matrixPosition.y - 1][matrixPosition.x] += matrix[matrixPosition.y][matrixPosition.x] + 1
        else:
            if matrix[matrixPosition.y - 1][matrixPosition.x] == 0:
                matrix[matrixPosition.y - 1][matrixPosition.x] += matrix[matrixPosition.y][matrixPosition.x] + 1
            if matrix[matrixPosition.y + 1][matrixPosition.x] == 0:
                matrix[matrixPosition.y + 1][matrixPosition.x] += matrix[matrixPosition.y][matrixPosition.x] + 1
        """ # Другая проверка

        """
        print("     ", end="")
        for i in range(len(matrix[0])):
            print(f'{i:03}', end="  ")
        print()
        c = 0
        for i in matrix:
            print(f'{c:02}', end="   ")
            for e in i:
                if e == None:
                    print(f"{0:03}", end="  ")
                else:
                    print(f"{e:03}", end="  ")
            c += 1
            print()
        print(pos.x, pos.y)
        print()
        print()
        print()
        """ # Вывод матрицы


        if pos.x == 0:
            l = len(matrix[0]) - 1
            if matrix[pos.y][l] == None:
                matrix[pos.y][l] = matrix[pos.y][pos.x] + 1
                self.checkAndMark(matrix, vec.Vector2(l, pos.y))
            if matrix[pos.y][pos.x] > matrix[pos.y][l] and matrix[pos.y][l] != -1:
                matrix[pos.y][pos.x] = matrix[pos.y][l] + 1
        else:
            if matrix[pos.y][pos.x - 1] == None:
                matrix[pos.y][pos.x - 1] = matrix[pos.y][pos.x] + 1
                self.checkAndMark(matrix, vec.Vector2(pos.x - 1, pos.y))
            if matrix[pos.y][pos.x] > matrix[pos.y][pos.x - 1] and matrix[pos.y][pos.x - 1] != -1:
                matrix[pos.y][pos.x] = matrix[pos.y][pos.x - 1] + 1

        if pos.x == len(matrix[0]) - 1:
            if matrix[pos.y][0] == None:
                matrix[pos.y][0] = matrix[pos.y][pos.x] + 1
                self.checkAndMark(matrix, vec.Vector2(0, pos.y))
            if matrix[pos.y][pos.x] > matrix[pos.y][0] and matrix[pos.y][0] != -1:
                matrix[pos.y][pos.x] = matrix[pos.y][0] + 1
        else:
            if matrix[pos.y][pos.x + 1] == None:
                matrix[pos.y][pos.x + 1] = matrix[pos.y][pos.x] + 1
                self.checkAndMark(matrix, vec.Vector2(pos.x + 1, pos.y))
            if matrix[pos.y][pos.x] > matrix[pos.y][pos.x + 1] and matrix[pos.y][pos.x + 1] != -1:
                matrix[pos.y][pos.x] = matrix[pos.y][pos.x + 1] + 1

        if matrix[pos.y - 1][pos.x] == None:
            matrix[pos.y - 1][pos.x] = matrix[pos.y][pos.x] + 1
            self.checkAndMark(matrix, vec.Vector2(pos.x, pos.y - 1))
        if matrix[pos.y][pos.x] > matrix[pos.y - 1][pos.x] and matrix[pos.y - 1][pos.x] != -1:
            matrix[pos.y][pos.x] = matrix[pos.y - 1][pos.x] + 1

        if matrix[pos.y + 1][pos.x] == None:
            matrix[pos.y + 1][pos.x] = matrix[pos.y][pos.x] + 1
            self.checkAndMark(matrix, vec.Vector2(pos.x, pos.y + 1))
        if matrix[pos.y][pos.x] > matrix[pos.y + 1][pos.x] and matrix[pos.y + 1][pos.x] != -1:
            matrix[pos.y][pos.x] = matrix[pos.y + 1][pos.x] + 1

        if pos.x == 0:
            l = len(matrix[0]) - 1
            if matrix[pos.y][l] - matrix[pos.y][pos.x] > 1:
                self.checkAndMark(matrix, vec.Vector2(l, pos.y))
        else:
            if matrix[pos.y][pos.x - 1] - matrix[pos.y][pos.x] > 1:
                self.checkAndMark(matrix, vec.Vector2(pos.x - 1, pos.y))
        if pos.x == len(matrix[0]) - 1:
            if matrix[pos.y][0] - matrix[pos.y][pos.x] > 1:
                self.checkAndMark(matrix, vec.Vector2(0, pos.y))
        else:
            if matrix[pos.y][pos.x + 1] - matrix[pos.y][pos.x] > 1:
                self.checkAndMark(matrix, vec.Vector2(pos.x + 1, pos.y))
        if matrix[pos.y - 1][pos.x] - matrix[pos.y][pos.x] > 1:
            self.checkAndMark(matrix, vec.Vector2(pos.x, pos.y - 1))
        if matrix[pos.y + 1][pos.x] - matrix[pos.y][pos.x] > 1:
            self.checkAndMark(matrix, vec.Vector2(pos.x, pos.y + 1))

    def buildPath(self, matrix, path, pos, endPos):
        if pos != endPos:
            if pos.x == 0:
                l = len(matrix[0]) - 1
                if matrix[pos.y][pos.x] - matrix[pos.y][l] == 1:
                    path.append(vec.Vector2(1, 0))
                    self.buildPath(matrix, path, vec.Vector2(l, pos.y), endPos)
            else:
                if matrix[pos.y][pos.x] - matrix[pos.y][pos.x - 1] == 1:
                    path.append(vec.Vector2(1, 0))
                    self.buildPath(matrix, path, vec.Vector2(pos.x - 1, pos.y), endPos)
            if pos.x == len(matrix[0]) - 1:
                if matrix[pos.y][pos.x] - matrix[pos.y][0] == 1:
                    path.append(vec.Vector2(-1, 0))
                    self.buildPath(matrix, path, vec.Vector2(0, pos.y), endPos)
            else:
                if matrix[pos.y][pos.x] - matrix[pos.y][pos.x + 1] == 1:
                    path.append(vec.Vector2(-1, 0))
                    self.buildPath(matrix, path, vec.Vector2(pos.x + 1, pos.y), endPos)
            if matrix[pos.y][pos.x] - matrix[pos.y - 1][pos.x] == 1:
                path.append(vec.Vector2(0, 1))
                self.buildPath(matrix, path, vec.Vector2(pos.x, pos.y - 1), endPos)
            if matrix[pos.y][pos.x] - matrix[pos.y + 1][pos.x] == 1:
                path.append(vec.Vector2(0, -1))
                self.buildPath(matrix, path, vec.Vector2(pos.x, pos.y + 1), endPos)
        else:
            return

    def return_time(self):
        return self.t

class GUIManager:
    def __init__(self, welcome_text="welcome to pac-man!"):
        self.instance = self
        self.welcoming_label = Label(70, 20, welcome_text)
        self.play_button = Button(274, 375, "play", False)
        self.quit_button = Button(274, 475)
        self.score_label = Label(318, 800, '0')

        if welcome_text == "you lost!":
            self.welcoming_label = Label(220, 20, welcome_text)

        if welcome_text == "you won!":
            self.welcoming_label = Label(220, 2, welcome_text)


    def LoadContent(self):
        self.welcoming_label.loadFont()
        self.play_button.Label.loadFont()
        self.quit_button.Label.loadFont()

    def Update(self):
        self.play_button.update()
        self.quit_button.update()

    def reInit(self, new_text):
        if new_text == "you lost!":
            self.welcoming_label = Label(220, 20, new_text)

        if new_text == "you won!":
            self.welcoming_label = Label(220, 20, new_text)

        self.LoadContent()
    def Draw(self):
        self.welcoming_label.draw()
        self.play_button.draw()
        self.quit_button.draw()
