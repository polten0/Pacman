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

    def addAnimation(self, texture, totalFrames, totalTime, isRepeat, name):  # Через него добавляем новые анимации
        self.animations.append(Animation(texture, totalFrames, totalTime, isRepeat, name))


    def getSourceRectangle(self, name):  # Используется для получения прямоугольника на текстурке.
        selectedAnimation = None
        for animation in self.animations:
            if animation.name == name:
                selectedAnimation = animation

        return pyray.Rectangle(selectedAnimation.currentFrame * selectedAnimation.width, 0,
                               selectedAnimation.width, selectedAnimation.height)

    def updateRectangles(self):  # Этот метод вызывает обьект в своем Update
        for animation in self.animations:
            if animation.interval - animation.elapsedTime <= 0:
                animation.currentFrame += 1
                animation.elapsedTime = 0
            if animation.currentFrame == animation.totalFrames:
                if animation.isRepeat:
                    animation.RepeatData()
                else:
                    self.animations.remove(animation)
                continue
            animation.elapsedTime += pyray.get_frame_time()
