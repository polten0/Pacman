import pyray
import vec

from ObjectClasses.GameObjects import Player, Food, BigFood, RedGhost
from ObjectClasses.Objects import GameObject
from ObjectClasses.MapObjects import Wall, Floor
from ObjectClasses.UIObjects import Label
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
        AppManager.instance = self

    def Initialization(self):
        pyray.init_window(AppManager.screenWidth, AppManager.screenHeight, 'Game')
        self.gameManager.LoadContent()

    def Update(self):
        self.gameManager.Update()

    def Draw(self):
        pyray.clear_background(pyray.BLACK)
        pyray.begin_drawing()

        self.gameManager.Draw()

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
        self.player_is_boosted = False
        self.score = 0
        self.mapManager = MapManager()
        self.Pacman = Player()
        self.scale = 3
        self.t = 0

        self.score_text = Label(10, 30, "SCORE:")
        self.score_label = Label(220, 30, str(self.score))

        self.ghosts = []
        ghost = RedGhost()
        ghost.matrixPosition = vec.Vector2(15, 8)
        self.ghosts.append(ghost)

    def Draw(self):
        self.score_text.draw()
        self.score_label.draw()
        self.mapManager.Draw()

        for ghost in self.ghosts:
            ghost.draw()
        self.Pacman.draw()

    def LoadContent(self):
        self.mapManager.loadContent()
        self.Pacman.loadContent()
        self.score_text.loadFont()
        self.score_label.loadFont()

        for ghost in self.ghosts:
            ghost.loadContent()

    def Update(self):
        self.t += 1

        self.Pacman.update()

        for ghost in self.ghosts:
            ghost.update()

        self.score_label.update(str(self.score))

    def ReturnObject(self, x, y):
        return self.mapManager.matrix[y][x].isCollide

    def ReturnFood(self, x, y):
        if(isinstance(self.mapManager.matrixFood[y][x], Food)):
            return self.mapManager.matrixFood[y][x].active

    def PrintObject(self, x, y):
        print(self.mapManager.matrix[y][x])

    def CheckCollision(self, object_a, object_b):
        if (object_a.matrixX == object_b.matrixX and object_a.matrixY == object_b.matrixY):
            object_a.OnCollision(object_b)
            object_b.OnCollision(object_a)

    def FoodCollision(self, PlayerObject):
        self.mapManager.matrixFood[PlayerObject.matrixY()][PlayerObject.matrixX()].onCollision()

    def boost_player(self):
        self.player_is_boosted = True

    def addScore(self, scoreObject):
        if (isinstance(scoreObject, Food)):
            self.score += 10
        if (isinstance(scoreObject, BigFood)):
            self.score += 50

    def getPlayerPos(self):
        return self.Pacman.matrixPosition

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
    def __init__(self):
        pass

    def Update(self):
        pass

    def Draw(self):
        pass
