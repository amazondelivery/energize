class Camera:

    def __init__(self, mapDimensions, initialFocus):
        self.mapDimensions = mapDimensions
        self.focus = [*initialFocus]

    def updateX(self, x):
        addend = self.focus[0] + x
        if addend < 0 or addend > self.mapDimensions[0]:
            return False
        else:
            self.focus[0] = addend
            return True

    def updateY(self, y):
        addend = self.focus[1] + y
        if addend < 0 or addend > self.mapDimensions[1]:
            return False
        else:
            self.focus[1] = addend
            return True

    def scan(self, playerCoords):
        print('placeholder')
        #increase acceleration of movement of camera the farther the player is from the camera focus

    def getFocusPosition(self):
        return self.focus

