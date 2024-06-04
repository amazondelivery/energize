from screenObject import Image
class Character():
    def __init__(self):
        self.speed = 4
        self.characterImage = None

    def blit(self):
        return self.characterImage.blit()

    def updatePos(self, x, y):
        self.characterImage.updatePos(x, y)

    def boundaryCollision(self, x, y):
        return 0

class Player(Character):
    def __init__(self, imageName, clickAction, dimensions, position = (True, 0, True, 0), sprites = ()):
        super().__init__()
        self.characterImage = Image(imageName, clickAction, position, dimensions)
        self.universalPosition = self.characterImage.getPos()
        self.dimensions = dimensions
        self.sprites = sprites

    def boundaryCollision(self, x, y):
        imageRect = self.characterImage.getRect()
        imageWidth = imageRect[2]
        imageHeight = imageRect[3]
        if (x != 0 and (self.universalPosition[0] + x < 0 or self.universalPosition[0] + x + imageWidth//2 > 1280)):
            return True
        elif (y != 0 and (self.universalPosition[1] - y < 0 or self.universalPosition[1] - y + imageHeight//2 > 720)):
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

    def getPosition(self):
        return self.characterImage.getPos()

