import pyray
from ObjectClasses.Objects import GameObject, MapObject, UIObject

class AppManager:
    instanse = None
    screenWidth = 500
    screenHeight = 700
    def __init__(self):
        self.gameManager = GameManager()
        AppManager.instanse = self

    def Initialization(self):
        pyray.init_window(AppManager.screenWidth, AppManager.screenHeight, 'Game')

    def Update(self):
        self.gameManager.Update()

    def Draw(self):
        pyray.clear_background(pyray.BLACK)
        pyray.begin_drawing()

        self.gameManager.Draw()

        pyray.end_drawing()

class MapManager:
    def __init__(self):
        pass

    def Draw(self):
        pass

class GameManager:
    def __init__(self):
        self.listGameObjects = list([GameObject()])


    def Update(self):
        for gameObject in self.listGameObjects:
            gameObject.update()

    def Draw(self):
        for gameObject in self.listGameObjects:
            gameObject.draw()

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
