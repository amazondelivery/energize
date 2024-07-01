import math
class Camera:

    def __init__(self, mapDimensions, initialFocus):
        self.mapDimensions = mapDimensions
        self.focus = [*initialFocus]
        self.pullDistance = 200

        self.accelerationX = 0
        self.accelerationY = 0

        self.velocityX = 0
        self.velocityY = 0

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

    def distanceFromPlayer(self, playerCoords):
        return math.sqrt((playerCoords[0] - self.focus[0])**2 + (playerCoords[1] - self.focus[1])**2)

    def distanceFromPlayerX(self, playerCoords):
        return playerCoords[0] - self.focus[0]

    def distanceFromPlayerY(self, playerCoords):
        return playerCoords[1] - self.focus[1]

    def getPlayerOffset(self, playerPosition):

        currentCameraFocus = self.getFocusPosition()
        return ((currentCameraFocus[0] - playerPosition[0]), (currentCameraFocus[1] - playerPosition[1]))


        accelerationConstant = 5

        distanceFromPlayerX = self.distanceFromPlayerX(playerPosition)
        distanceFromPlayerY = self.distanceFromPlayerY(playerPosition)
        self.accelerationX = distanceFromPlayerX / accelerationConstant
        self.accelerationY = distanceFromPlayerY / accelerationConstant

        self.velocityX += self.accelerationX
        self.velocityY += self.accelerationY

        positionX = currentCameraFocus[0] - self.velocityX
        positionY = currentCameraFocus[1] - self.velocityY

        return (positionX, positionY)

    def scan(self, playerCoords):
        if self.distanceFromPlayer(playerCoords) > self.pullDistance:
            x = playerCoords[0] - self.focus[0]
            y = playerCoords[1] - self.focus[1]

        #increase acceleration of movement of camera the farther the player is from the camera focus

    def getFocusPosition(self):
        return self.focus

