import pyray


class AppManager:
    screenWidth = 500
    screenHeight = 700
    def init(self):
        pass

    def Initialization(self):
        pyray.init_window(AppManager.screenWidth, AppManager.screenHeight, 'Game')

    def Update(self):
        pyray.clear_background(pyray.BLACK)

    def Draw(self):
        pyray.begin_drawing()

        pyray.end_drawing()