import math
class Camera:

    def __init__(self, mapDimensions, initialFocus):
        self.mapDimensions = mapDimensions
        self.focus = [*initialFocus]
        self.pullDistance = 200

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

    def moveLeft(self, distance):
        print("")

    def moveRight(self, distance):
        print('')

    def moveUp(self, distance):
        print()

    def moveDown(self, distance):
        print()

    def distanceFromPlayer(self, playerCoords):
        return math.sqrt((playerCoords[0] - self.focus[0])**2 + (playerCoords[1] - self.focus[1])**2)

    def getPlayerOffset(self, character):
        currentCameraFocus = self.getFocusPosition()
        playerPosition = character.getUniversalPosition()
        return (currentCameraFocus[0] - playerPosition[0], currentCameraFocus[1] - playerPosition[1])

    def scan(self, playerCoords):
        if self.distanceFromPlayer(playerCoords) > self.pullDistance:
            x = playerCoords[0] - self.focus[0]
            y = playerCoords[1] - self.focus[1]

        #increase acceleration of movement of camera the farther the player is from the camera focus

    def getFocusPosition(self):
        return self.focus

