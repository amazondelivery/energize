from gameStructure.asset import Image, Asset


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


runSprites = ("leftFoot.png", "rightFoot.png")

class Player(Character):

    def __init__(self, assetFolder, dimensions, default = "stand.png",
                 position = (True, 0, True, 0), map_dimensions = (), speed = 15,
                 range = 350, clickAction = -1):
        super().__init__()
        self.default = Image("assets/images/player/" + default, position, dimensions, transparent=True)
        self.frontRuns = (Image("assets/images/player/" + runSprites[0], position, dimensions, transparent=True),
                          Image("assets/images/player/" + runSprites[1], position, dimensions, transparent=True))

        self.characterImage = self.default
        self.universalPosition = self.universalPositionGetter(self.characterImage.getPosition(), dimensions)
        self.dimensions = dimensions
        self.mapDimensions = map_dimensions
        self.speed = speed

        self.range = range

    def universalPositionGetter(self, initialPosition, dimensions):
        initialPosition[0] += dimensions[0] // 2
        initialPosition[1] += dimensions[1] // 2
        return initialPosition

    def getRect(self):
        return self.characterImage.getRect()

    def getRange(self):
        return self.range

    def getSpeed(self):
        return self.speed

    def updatePos(self, changeX, changeY):
        self.universalPosition[0] += changeX
        self.universalPosition[1] -= changeY

    def getUniversalPosition(self):
        return self.universalPosition

    def getPosition(self):
        return self.characterImage.getPosition()

    def updatePos(self, x, y):
        self.default.updatePosition(x,y)
        for thing in self.frontRuns:
            thing.updatePosition(x,y)

    def updateCharacterImage(self, number):
        self.characterImage = self.frontRuns[number % 2]
