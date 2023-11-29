import pyray
import vec

from ObjectClasses.GameObjects import Player, Food, BigFood, Ghost
from ObjectClasses.Objects import GameObject, MapObject, UIObject
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
        self.player_is_boosted = False
        self.score = 0
        self.mapManager = MapManager()
        self.Pacman = Player()
        self.scale = 3
        self.t = 0
        self.score_text = Label(10, 30, "SCORE:")
        self.score_label = Label(220, 30, str(self.score))

    def Draw(self):
        self.score_text.draw()
        self.score_label.draw()
        self.mapManager.Draw()
        self.Pacman.draw()


    def LoadContent(self):
        self.mapManager.loadContent()
        self.Pacman.loadContent()
        self.score_text.loadFont()
        self.score_label.loadFont()

    def CheckAllFood(self):
        checksum = 0
        for gameObjects in self.mapManager.matrixFood:
            for Foods in gameObjects:
                if (isinstance(Foods, Food)):
                    if not (Foods.active):
                        checksum += 1
                    else:
                        checksum = 0
        if (checksum != 0):
            AppManager.instance.SwitchState("menu")
            AppManager.instance.GUIManager.reInit("you won!")

    def Update(self):
        self.t += 1

        self.Pacman.update()
        self.score_label.update(str(self.score))
        if (self.score >= 3280):
            self.CheckAllFood()

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

    def gameOver(self):
        pass

    def addScore(self, scoreObject):
        if (isinstance(scoreObject, Food)):
            self.score += 10
        if (isinstance(scoreObject, BigFood)):
            self.score += 50

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
            self.welcoming_label = Label(220, 2, new_text)

        self.LoadContent()
    def Draw(self):
        self.welcoming_label.draw()
        self.play_button.draw()
        self.quit_button.draw()
