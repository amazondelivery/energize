from asset import Image

class Character():
    def __init__(self):
        self.speed = 4
        self.characterImage = None

    def blit(self, offset = (0,0)):
        return self.characterImage.blit(offset) #

    def updatePos(self, x, y):
        self.characterImage.updatePosition(x, y)

    def boundaryCollision(self, x, y):
        return 0

class Player(Character):

    def universalPositionGetter(self, initialPosition, dimensions):
        initialPosition[0] += dimensions[0] // 2
        initialPosition[1] += dimensions[1] // 2
        return initialPosition

    def __init__(self, imageName, clickAction,
                 dimensions, position = (True, 0, True, 0),
                 sprites = (), map_dimensions = (), speed = 15, range = 350):
        super().__init__()
        self.characterImage = Image(imageName, clickAction, position, dimensions)
        self.universalPosition = self.universalPositionGetter(self.characterImage.getPosition(), dimensions)
        self.dimensions = dimensions
        self.sprites = sprites
        self.mapDimensions = map_dimensions
        self.speed = speed

        self.range = range


    def getRect(self):
        return self.characterImage.getRect()

    def getRange(self):
        return self.range

    def getSpeed(self):
        return self.speed

    def updatePos(self, changeX, changeY):
        self.universalPosition[0] += changeX
        self.universalPosition[1] -= changeY

    def testUpdatedPos(self, x, y):
        return (self.universalPosition[0] + x, self.universalPosition[1] - y)

    def changeImage(self, newImage):
        prevImage = self.characterImage
        self.characterImage = Image(newImage, prevImage.getAction(), prevImage.getPosition(), self.dimensions)

    def getUniversalPosition(self):
        return self.universalPosition

    def getPosition(self):
        return self.characterImage.getPosition()