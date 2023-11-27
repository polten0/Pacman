import pyray
import vec
import os
from ObjectClasses.Objects import UIObject

class Label(UIObject):
    def __init__(self, x = 0, y = 0, text="null"):
        super().__init__()
        self.Font = pyray.load_font(f"{os.getcwd()}/Content/Font/joystix monospace.ttf")
        self.Text = text
        self.FontSize = 10
        self.Spacing = 1
        self.X(x)
        self.Y(y)

    def draw(self):
        pyray.draw_text_ex(self.Font, self.Text, self.X, self.Y, self.FontSize, self.Spacing, pyray.WHITE)

    def update(self, new_text):
        self.Text = new_text
        pyray.draw_text_ex(self.Font, self.Text, self.X, self.Y, self.FontSize, self.Spacing, pyray.WHITE)
