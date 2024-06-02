from scenes import *
from abc import ABC, abstractmethod

class Sequence(ABC):

    screen_width = 1280
    screen_height = 720
    @abstractmethod
    def __init__(self):
        self.fonts = {}
        self.texts = []
        self.images = []

    @abstractmethod
    def record(self, char):
        pass

    @abstractmethod
    def mouse(self, coords, buttonsPressed):
        pass

    @abstractmethod
    def drawHelper(self, screen):
        pass

    def draw(self, screen):
        screen = self.drawHelper(screen)
        self.blit(screen)
        return screen

    def addSizes(self):
        for text in self.texts.keys():
            self.texts[text].append(self.sizes[text])
        for image in self.images.keys():
            self.images[image].append(self.sizes[image])
        self.sizes = None #disposes of the dict sizes

    def blit(self, screen):
        for image in self.images:
            screen.blit(*image.blit()) #test value
        for text in self.texts:
            screen.blit(*text.blit())
        for character in self.characters:
            screen.blit(*character.blit())

    def font(self, fontName, fontSize):
        return pg.font.Font(fontName, fontSize)

    def checkCollision(self, mouseClickCoords):

        for text in self.texts:
            xText, yText, textLength, textHeight = text.getRect()
            xMouse = mouseClickCoords[0]
            yMouse = mouseClickCoords[1]
            xInit, yInit = text.getPos()

            if ((xText + xInit <= xMouse <= xText + xInit + textLength)
                    and (yText + yInit <= yMouse <= yText + yInit + textHeight)):
                return text

        return None

    def mouse(self, coords, buttonsPressed):
        collisionButton = self.checkCollision(coords)
        if buttonsPressed[0] == True and collisionButton != None:
            return collisionButton.getAction()
        return -1

#java's abstract classes would be perfect here. real shame...
