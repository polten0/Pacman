import pyray
import vec
import os
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
