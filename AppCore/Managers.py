import pyray
from ObjectClasses.Objects import GameObject, MapObject, UIObject
from ObjectClasses.MapObjects import Wall
from AppCore import Interfaces
import json
import os


class AppManager:
    instance = None
    screenWidth = 500
    screenHeight = 700
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
        self.listMapObjects = list([])

        self.loadMap()

    def loadContent(self):
        for mapObject in self.listMapObjects:
            if isinstance(mapObject, Interfaces.ITextureableObject):
                mapObject.loadContent()

    def Draw(self):
        for mapObject in self.listMapObjects:
            mapObject.draw()

    def loadMap(self):
        map = open(f"{os.getcwd()}/Content/Maps/Map1.json").read()
        mapdict = json.loads(map)

        tilesets = mapdict["tilesets"]

        for tileset in tilesets:
            mapObject = MapObject()

            mapObject.filepath = tileset["source"]
            mapObject.size = tileset["tilewidth"]

            self.listMapObjects.add(mapObject)

class GameManager:
    def __init__(self):
        self.mapManager = MapManager()
        self.listGameObjects = list([])

    def LoadContent(self):
        self.mapManager.loadContent()

    def Update(self):
        for gameObject in self.listGameObjects:
            gameObject.update()

    def Draw(self):
        for gameObject in self.listGameObjects:
            gameObject.draw()
        self.mapManager.Draw()

    def CheckCollision(self):
        for gameObject in self.listGameObjects:
            gameObject.update()
class GUIManager:
    def __init__(self):
        pass

    def Update(self):
        pass

    def Draw(self):
        pass
