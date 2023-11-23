class Animation:
    def config(self, textureName, totalFrames):
        self.currentFrame = 0
        self.totalFrames = totalFrames
        self.textureName = textureName

    def __init__(self, textureName, totalFrames):
        self.config(textureName, totalFrames)

class Animator:
    def __init__(self):
        self.Animations = None