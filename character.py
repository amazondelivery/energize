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
