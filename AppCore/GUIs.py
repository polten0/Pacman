class GUI:
    def __init__(self):
        self.listUIObjects = list()

    def Update(self):
        for UIObject in self.listUIObjects:
            UIObject.update()

    def Draw(self):
        for UIObject in self.listUIObjects:
            UIObject.draw()