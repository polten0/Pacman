import pyray
import vec
import os
import AppCore.Managers
from ObjectClasses.Objects import UIObject

class Label(UIObject):
    def __init__(self, x = 0, y = 0, text="null"):
        super().__init__()
        self.Text = text
        self.Font = None
        self.fontPath = ""
        self.FontSize = 40
        self.Spacing = 1
        self.X = x
        self.Y = y


    def draw(self):
        pyray.draw_text_ex(self.Font, self.Text, pyray.Vector2(self.X, self.Y), self.FontSize, self.Spacing, pyray.WHITE)

    def update(self, new_text):
        self.Text = new_text

    def loadFont(self):
        self.fontPath = f"{os.getcwd()}/Content/Font/joystix monospace.ttf"
        self.Font = pyray.load_font(self.fontPath)


class Button(UIObject):
    def __init__(self, x=0, y=0, text="quit", q=True):
        super().__init__()
        self.Quit = q
        self.X = x
        self.Y = y
        self.width = 130
        self.height = 50
        self.Label = Label(self.X + 10, self.Y + 5, text)
        if not self.Quit:
            self.Label.Text = "play"

    def quit(self):
        pyray.close_window()

    def play(self):
        AppCore.Managers.AppManager.instance.SwitchState("game")

    def MouseProcessor(self):
        if(pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT)):
            if (pyray.check_collision_point_rec(pyray.get_mouse_position(), pyray.Rectangle(self.X, self.Y, self.width, self.height))):
                if (self.Quit):
                    self.quit()
                elif not (self.Quit):
                    self.play()
    def loadFont(self):
        self.Label.fontPath = f"{os.getcwd()}/Content/Font/joystix monospace.ttf"
        self.Label.Font = pyray.load_font(self.Label.fontPath)

    def update(self):
        self.MouseProcessor()

    def draw(self):
        pyray.draw_rectangle_rounded_lines(pyray.Rectangle(self.X, self.Y, self.width, self.height), 1.0, 10, 2, pyray.BLUE)
        self.Label.draw()






