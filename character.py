from screenObject import Image
class Character():
    def __init__(self):
        self.speed = 4
        self.characterImage = None

    def blit(self, offset = (0,0)):
        return self.characterImage.blit(offset)

    def updatePos(self, x, y):
        self.characterImage.updatePos(x, y)

    def boundaryCollision(self, x, y):
        return 0

class Player(Character):

    def universalPositionGetter(self, initialPosition, dimensions):
        initialPosition[0] += dimensions[0] //2
        initialPosition[1] += dimensions[1] // 2
        return initialPosition

    def __init__(self, imageName, clickAction, dimensions, position = (True, 0, True, 0), sprites = ()):
        super().__init__()
        self.characterImage = Image(imageName, clickAction, position, dimensions)
        self.universalPosition = self.universalPositionGetter(self.characterImage.getPos(), dimensions)
        self.dimensions = dimensions
        self.sprites = sprites

    def boundaryCollision(self, x, y):
        imageRect = self.characterImage.getRect()
        imageWidth = imageRect[2]
        imageHeight = imageRect[3]
        if (x != 0 and (self.universalPosition[0] + x < 0 or self.universalPosition[0] + x + imageWidth//2 > 1280 * 12)):
            return True
        elif (y != 0 and (self.universalPosition[1] - y < 0 or self.universalPosition[1] - y + imageHeight//2 > 720 * 24)):
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
