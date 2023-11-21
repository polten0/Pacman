import pyray
from ObjectClasses.Objects import GameObject, MapObject, UIObject

class AppManager:
    instance = None
    screenWidth = 500
    screenHeight = 700
    def __init__(self):
        self.gameManager = GameManager()
        AppManager.instance = self

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
        self.player_is_boosted = False
        self.score = 0


    def Update(self):
        for gameObject in self.listGameObjects:
            gameObject.update()

    def Draw(self):
        for gameObject in self.listGameObjects:
            gameObject.draw()

    def CheckCollision(self, object_a, object_b):
        if (pyray.check_collision_recs(object_a.rec, object_b.rec)):
            object_a.OnCollision(object_b)
            object_b.OnCollision(object_a)

    def boost_player(self):
        player_is_boosted = True
        pass

    def addScore(self, typeObject):
        if (typeObject == 'food'):
            self.score += 10
        if (typeObject == 'big_food'):
            self.score += 50


class GUIManager:
    def __init__(self):
        pass

    def Update(self):
        pass

    def Draw(self):
        pass
