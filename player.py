from character import Character
from screenObject import *

class Player(Character):

    def universalPositionGetter(self, initialPosition, dimensions):
        initialPosition[0] += dimensions[0] //2
        initialPosition[1] += dimensions[1] // 2
        return initialPosition

    def __init__(self, imageName, clickAction, dimensions, position = (True, 0, True, 0), sprites = (), map_dimensions = ()):
        super().__init__()
        self.characterImage = Image(imageName, clickAction, position, dimensions)
        self.universalPosition = self.universalPositionGetter(self.characterImage.getPos(), dimensions)
        self.dimensions = dimensions
        self.sprites = sprites
        self.mapDimensions = map_dimensions

    def boundaryCollision(self, x, y):
        imageRect = self.characterImage.getRect()
        imageWidth = imageRect[2]
        imageHeight = imageRect[3]
        if (x != 0 and (self.universalPosition[0] + x < 0 or self.universalPosition[0] + x + imageWidth > self.mapDimensions[0])):
            return True
        elif (y != 0 and (self.universalPosition[1] - y < 0 or self.universalPosition[1] - y + imageHeight > self.mapDimensions[1])):
            return True
        else:
            return False

    def updatePos(self, x, y):
        if not self.boundaryCollision(x, y):
            super().updatePos(x, y)
            self.universalPosition[0] += x
            self.universalPosition[1] -= y

    def changeImage(self, newImage):
        prevImage = self.characterImage
        self.characterImage = Image(newImage, prevImage.getAction(), prevImage.getPos(), self.dimensions)

    def getUniversalPosition(self):
        return self.universalPosition

    def getPosition(self):
        return self.characterImage.getPos()

