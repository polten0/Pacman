import pyray
import os
class Animation:
    def __init__(self, textureName, totalFrames, name):
        self.textureName = textureName
        self.totalFrames = totalFrames
        self.texture = None
        self.width = None
        self.height = None
        self.currentFrame = 0
        self.name = name

    def loadContent(self):
        self.texture = pyray.load_texture(f"{os.getcwd()}/Content/{self.textureName}")

        self.width = self.texture.width / self.totalFrames
        self.height = self.texture.height

class Animator:
    def __init__(self):
        self.animations = list([])

    def loadContent(self):
        for animation in self.animations:
            animation.loadContent()
