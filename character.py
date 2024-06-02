from screenObject import Image
class Character():
    def __init__(self):
        self.speed = 4
        self.characterImage = None #tbd

    def blit(self):
        return self.characterImage.blit()

    def updatePos(self, x, y):
        self.characterImage.updatePos(x, y)

class Player(Character):
    def __init__(self, imageName, clickAction, dimensions, position = (True, 0, True, 0)):
        super().__init__()
        self.characterImage = Image(imageName, clickAction, position, dimensions)

