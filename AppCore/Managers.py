import pyray
import vec

from ObjectClasses.GameObjects import Player, Food, BigFood, Ghost
from ObjectClasses.Objects import GameObject, MapObject, UIObject
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
        self.listGameObjects = list([GameObject()])
        self.player_is_boosted = False
        self.score = 0
        self.mapManager = MapManager()
        self.listGameObjects = list([])
        self.Pacman = Player()
        self.pacman_position = vec.Vector2(x = self.Pacman.matrixX(), y = self.Pacman.matrixY())
        self.scale = 3
        self.t = 0
        self.score_text = Label(10, 30, "SCORE:")
        self.score_label = Label(220, 30, str(self.score))

    def Draw(self):
        for gameObject in self.listGameObjects:
            gameObject.draw()

        self.score_text.draw()
        self.score_label.draw()
        self.mapManager.Draw()
        self.Pacman.draw()


    def LoadContent(self):
        self.mapManager.loadContent()
        self.Pacman.loadContent()
        self.score_text.loadFont()
        self.score_label.loadFont()

    def Update(self):
        self.t += 1
        for gameObject in self.listGameObjects:
            gameObject.update()
        self.Pacman.update()
        self.score_label.update(str(self.score))

    def ReturnObject(self, x, y):
        return self.mapManager.matrix[y][x].isCollide

    def ReturnFood(self, x, y):
        return self.mapManager.matrixFood[y][x].active



    def PrintObject(self, x, y):
        print(self.mapManager.matrix[y][x])

    def CheckCollision(self, object_a, object_b):
        if (object_a.matrixX == object_b.matrixX and object_a.matrixY == object_b.matrixY):
            object_a.OnCollision(object_b)
            object_b.OnCollision(object_a)

    def boost_player(self):
        self.player_is_boosted = True

    def addScore(self, scoreObject):
        if (isinstance(scoreObject, Food)):
            self.score += 10
        if (isinstance(scoreObject, BigFood)):
            self.score += 50

    def return_time(self):
        return self.t

class GUIManager:
    def __init__(self):
        pass

    def Update(self):
        pass

    def Draw(self):
        pass
