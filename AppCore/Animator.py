import pyray
import os
class Animation: # По сути просто контейнер информации о анимации.
    def __init__(self, texture=None, totalFrames=1, totalTime=1, isRepeat=True, name=""):
        self.texture = texture
        self.totalFrames = totalFrames
        self.width = self.texture.width / self.totalFrames
        self.height = self.texture.height
        self.currentFrame = 0
        self.totalTime = totalTime
        self.interval = self.totalTime / self.totalFrames
        self.elapsedTime = 0
        self.isRepeat = isRepeat
        self.name = name

    def RepeatData(self):
        self.elapsedTime = 0
        self.currentFrame = 0

class Animator:  # Контролирует состояние анимаций. Создаем и засовываем в него анимации с помощью метода addAnimation
    def __init__(self):
        self.animations = list([])
        self.elapsedTime = 0

    def addAnimation(self, texture, totalFrames, totalTime, name):  # Через него добавляем новые анимации
        self.animations.append(Animation(texture, totalFrames, totalTime, name))

    def getSourceRectangle(self, name):  # Используется для получения прямоугольника на текстурке.
        selectedAnimation = None
        for animation in self.animations:
            if animation.name == name:
                selectedAnimation = animation

        return pyray.Rectangle(x=selectedAnimation.currentFrame * selectedAnimation.width, y=0,
                               width=selectedAnimation.width, height=selectedAnimation.height)

    def updateRectangles(self):  # Этот метод вызывает обьект в своем Update
        for animation in self.animations:
            if animation.interval / self.elapsedTime >= 1:
                animation.currentFrame += 1
        self.elapsedTime += pyray.get_frame_time()