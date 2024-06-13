#at some point i want the world to be randomly generated with a seed
from tile import Tile
from asset import *
from camera import *
from gradient import *
from timeController import TimeController


class World:
    def __init__(self, map, assets, player, mapDimensions = (0, 0), initialCameraPoint = (0,0)):

        #error-checking
        if mapDimensions[0] == 0 or mapDimensions[1] == 0:
            raise NotImplementedError

        #making camera and gradients
        self.map_width, self.map_height = mapDimensions
        self.screen_width, self.screen_height = 1280, 720
        self.camera = Camera((self.map_width, self.map_height), initialCameraPoint)
        self.gradients = GameGradients()

        #images that the tiles will use
        self.map = map
        self.assets = assets
        self.player = player
        self.timeController = TimeController()

        self.structures = [
            #test
            Image("solarBright.png", -1, (False, 800, False, 800), transformation = (80,80))
        ]

        #creates tilemap of width // 40 and height // 40)
        self.tileMap = [ [Tile()] * (mapDimensions[1] // 80) for i in range(mapDimensions[0] // 80) ]

        self.mapDimensions = mapDimensions

    def getPlayer(self):
        return self.player

    def updatePlayer(self, changeX, changeY):
        if self.checkCollision(changeX, changeY) == False:
            self.player.updatePos(changeX, changeY)

    def renderTiles(self):
        for rowNum, tileRow in enumerate(self.tileMap):
            for columnNum, tile in enumerate(tileRow):
                print('test')


    def checkCollision(self, playerChangeX, playerChangeY):
        if self.mapCollision(playerChangeX, playerChangeY):
            return True
        elif self.objectCollision(playerChangeX, playerChangeY):
            return True
        else:
            return False

    def mapCollision(self, changeX, changeY):
        playerRect = self.player.getRect()
        if changeX == 0:
            newY = self.player.getPosition()[1] - changeY
            if (newY - playerRect[3] // 2 < 0 or newY + playerRect[3] // 2 > self.mapDimensions[1]):
                return True
        else:
            newX = self.player.getPosition()[0] + changeX
            if (newX - playerRect[2] // 2 < 0 or newX + playerRect[2] // 2 > self.mapDimensions[0]):
                return True
        return False

    def objectCollision(self, changeX, changeY):
        #https://silentmatt.com/rectangle-intersection/
        #used the above link to help
        playerPosition = self.player.getPosition()
        objectWiggleRoom = 0 #probably not needed
        playerWidth, playerHeight = self.player.getRect()[2:4]
        paddingValue = 1 #normally 5/4
        pX1 = playerPosition[0] + changeX * paddingValue - playerWidth // 2
        pX2 = playerPosition[0] + changeX * paddingValue + playerWidth // 2
        pY1 = playerPosition[1] - changeY * paddingValue - playerHeight // 2
        pY2 = playerPosition[1] - changeY * paddingValue + playerHeight // 2

        for object in self.structures:
            objectPosition = object.getPosition()
            objectWidth, objectHeight = object.getRect()[2:4]
            oX1 = objectPosition[0] - objectWidth // 2 + objectWiggleRoom
            oX2 = objectPosition[0] + objectWidth // 2 - objectWiggleRoom
            oY1 = objectPosition[1] - objectHeight // 2 + objectWiggleRoom
            oY2 = objectPosition[1] + objectHeight // 2 - objectWiggleRoom

            if (pX1 < oX2 and pX2 > oX1 and pY1 < oY2 and pY2 > oY1):
                return True

        return False

    def getMap(self):
        return self.map

    def getPlayerTile(self):
        position = self.player.getUniversalPosition()
        return (position[0] // 80, position[1] // 80)

    def addSolarPanel(self, tilePositionIndexRow, tilePositionIndexColumn):
        tile = self.tileMap[tilePositionIndexRow][tilePositionIndexColumn]
        if tile.isEmpty():
            tile.solarify()
            return True
        else:
            return False


    def getCamera(self):
        return self.camera

    def getGradientColor(self, gradientTitle):
        gradient = self.gradients.getGradient(gradientTitle)
        time = self.timeController.getTime()
        color = gradient.getColor((time // (gradient.getTimeStop() * 10)) % gradient.getNumStops())
        return color

    def getStructures(self):
        return self.structures

    def timeIncrease(self):
        self.timeController.timeIncrease()

    def getCameraOffset(self):
        return self.camera.getPlayerOffset(self.player.getPosition())

    def getTileOfCoord(self, mapCoords):
        return self.tileMap[mapCoords[0] // 80][mapCoords[0] // 80]

    def click(self, frameCoords, mapCoords):
        if (mapCoords[0] < 0 or mapCoords[0] > self.map_width or mapCoords[1] < 0 or mapCoords[1] > self.map_height):
            tile = self.getTileOfCoord(mapCoords)
            #map coord click is valid
        else:
            #invalid
            return None






