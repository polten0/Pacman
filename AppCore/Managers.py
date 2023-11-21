import pyray
from ObjectClasses.Objects import GameObject, MapObject, UIObject
from ObjectClasses.MapObjects import Wall
from AppCore import Interfaces

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
        self.listMapObjects = list([Wall()])

    def loadContent(self):
        for mapObject in self.listMapObjects:
            if isinstance(mapObject, Interfaces.ITextureableObject):
                mapObject.loadContent()

    def Draw(self):
        for mapObject in self.listMapObjects:
            mapObject.draw()

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
