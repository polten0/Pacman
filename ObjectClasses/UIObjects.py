import pyray
import vec
import os
from ObjectClasses.Objects import UIObject

class Label(UIObject):
    def __init__(self, text="null"):
        super().__init__()
        self.Font = pyray.load_font(f"{os.getcwd()}/Content/Font/joystix monospace.ttf")
        self.Text = "text"
        self.FontSize = 10
        self.Spacing = 1
        self.X(10)
        self.Y(600)

    def draw(self):
        pyray.draw_text_ex(self.Font, self.Text, self.X, self.Y, self.fontSize, pyray.WHITE)
