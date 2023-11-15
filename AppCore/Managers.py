import pyray


class AppManager:
    screenWidth = 500
    screenHeight = 700
    def __init__(self):
        self.gameManager = GameManager()

    def Initialization(self):
        pyray.init_window(AppManager.screenWidth, AppManager.screenHeight, 'Game')

    def Update(self):
        pyray.clear_background(pyray.BLACK)

    def Draw(self):
        pyray.begin_drawing()

        pyray.end_drawing()

class GameManager:
    def __init__(self):
        self.listGameObjects = list()

    def Update(self):
        for gameObject in self.listGameObjects:
            gameObject.update()

    def Draw(self):
        for gameObject in self.listGameObjects:
            gameObject.draw()
