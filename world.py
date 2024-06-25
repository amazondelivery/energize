from tile import Tile
from structure import Structure
from camera import *
from gradient import *
from timeController import TimeController
from inventory import Inventory
from utils import *
# at some point i want the world to be randomly generated with a seed


class World:

    tileDim = 80
    gradients = GameGradients()
    structureCode = BidirectionalDict({
            0 : "none",
            1 : "solar",
            2 : "wind",
            3 : "windHelper"
        })

    def __init__(self, gameMap, assets, player, mapDimensions = (0, 0), initialCameraPoint = (0, 0)):

        # error-checking
        if mapDimensions[0] == 0 or mapDimensions[1] == 0:
            raise NotImplementedError

        # making camera and gradients
        self.map_width, self.map_height = mapDimensions
        self.screen_width, self.screen_height = 1280, 720
        self.camera = Camera((self.map_width, self.map_height), initialCameraPoint)

        # images that the tiles will use
        self.map = gameMap
        self.assets = assets
        self.player = player
        self.timeController = TimeController()

        # creates tilemap of width // 40 and height // 40) and initializes structures from previous playthrough
        self.tileMap = [[Tile()] * (self.map_width // self.tileDim) for _ in range(self.map_height // self.tileDim)]
        self.structures = self.initializeTileWorldStructures()
        self.guiIcons = [

        ]
        self.mapDimensions = mapDimensions

        #player settings
        self.currentSelection = 0
        self.numItems = 2
        startingInventory = {
            0 : 999999,
            1 : 15
        }
        self.inventory = Inventory(self.structureCode, startingInventory)

        # testing
        self.numSolarPanels = 15

    def getPlayer(self):
        return self.player

    def getActualCurrentSelection(self):
        return self.currentSelection % self.numItems

    def getCurrentSelection(self):
        return self.currentSelection

    def initializeStructure(self, typeOfStructure, coords):
        return 0

    def initializeTileWorldStructures(self):
        structures = []
        for rowNum, tileRow in enumerate(self.tileMap):
            for columnNum, tile in enumerate(tileRow):
                if tile.getType() != 0:
                    tileCoords = self.getCoordsOfTile(columnNum, rowNum)
                    structures.append(self.initializeStructure(type, tileCoords))
        return structures

    def updatePlayer(self, changeX, changeY):
        if not self.checkCollision(changeX, changeY):
            self.player.updatePos(changeX, changeY)

    def renderTiles(self):
        for rowNum, tileRow in enumerate(self.tileMap):
            for columnNum, tile in enumerate(tileRow):
                print('test')

    def checkCollision(self, playerChangeX, playerChangeY):
        if self.mapCollision(playerChangeX, playerChangeY) or self.objectCollision(playerChangeX, playerChangeY):
            return True
        else:
            return False

    def getMap(self):
        return self.map

    def getPlayerTile(self):
        position = self.player.getUniversalPosition()
        return (self.getTileLocationOfCoord(position))

    def getCamera(self):
        return self.camera

    def updateSelectedItem(self, y):
        if (self.currentSelection + y) % 2 != self.currentSelection % 2:
            self.currentSelection = (self.currentSelection + y) % 2

    def getSelectedItem(self):
        return self.currentSelection % self.numItems

    def getGradientColor(self, gradientTitle):
        gradient = self.gradients.getGradient(gradientTitle)
        time = self.timeController.getTime()
        color = gradient.getColor((time // (gradient.getTimeStop() * 10)) % gradient.getNumStops())
        return color

    def getStructures(self):
        return self.structures

    def timeIncrease(self):
        self.timeController.timeIncrease()

    def click(self, frameCoords, mapCoords):
        if not (self.outOfMapBounds(mapCoords) or self.inPlayersWay(mapCoords)):
            self.place(mapCoords)
        else:
            print('wah')
            return None

    def place(self, mapCoords):
        mapTile = self.getTileLocationOfCoord(mapCoords)
        objectPosition = self.getCoordsOfTile(*mapTile)
        if self.structureCode.get(self.getActualCurrentSelection()) == "solar" and self.numSolarPanels > 0:
            self.structures.append(Structure("solarDay.png", -1, (False, objectPosition[0], False, objectPosition[1])))
            self.numSolarPanels -= 1
            print(self.numSolarPanels)


    def hover(self, frameCoords, mapCoords):
        if not self.outOfMapBounds(mapCoords):
            # i want a yellow rectangle to border the tile hovered overs
            tileTuple = self.getTileLocationOfCoord(mapCoords)

    def getCameraOffset(self):
        return self.camera.getPlayerOffset(self.player.getPosition())

    def getTileOfCoord(self, mapCoords):
        location = self.getTileLocationOfCoord(mapCoords)
        return self.tileMap[location[1]][location[0]]


    def getTileLocationOfCoord(self, mapCoords):
        return (mapCoords[0] // self.tileDim, mapCoords[1] // self.tileDim)

    def getCoordsOfTile(self, col, row):
        return (col * self.tileDim, row * self.tileDim)

    def getLocationOfTile(self, tile):
        # avoid using this
        for rowNum, tileRow in enumerate(self.tileMap):
            for columnNum, tileIterate in enumerate(tileRow):
                print(columnNum, rowNum)
                if tile == tileIterate:
                    return (columnNum, rowNum)

    def outOfMapBounds(self, mapCoords):
        x = mapCoords[0]
        y = mapCoords[1]

        if (x < 0 or x > self.map_width or y < 0 or y > self.map_height):
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

    def inPlayersWay(self, mapCoords):

        mapTile = self.getTileLocationOfCoord(mapCoords)
        playerTile = self.getPlayerTile()
        if mapTile[0] == playerTile[0] and mapTile[1] == playerTile[1]:
            return True

        playerPosition = self.player.getUniversalPosition()
        playerWidth, playerHeight = self.player.getRect()[2:4]
        pX1 = playerPosition[0] - playerWidth // 2
        pX2 = playerPosition[0] + playerWidth // 2
        pY1 = playerPosition[1]  - playerHeight // 2
        pY2 = playerPosition[1] + playerHeight // 2

        objectPosition = self.getCoordsOfTile(*mapTile)
        oX1 = objectPosition[0]
        oX2 = objectPosition[0] + self.tileDim
        oY1 = objectPosition[1]
        oY2 = objectPosition[1] + self.tileDim

        if (pX1 < oX2 and pX2 > oX1 and pY1 < oY2 and pY2 > oY1):
            return True
        else:
            return False


    def objectCollision(self, changeX, changeY):
        # https://silentmatt.com/rectangle-intersection/
        # used the above link to help
        playerPosition = self.player.getPosition()
        objectWiggleRoom = 0  # probably not needed
        playerWidth, playerHeight = self.player.getRect()[2:4]
        paddingValue = 1  # normally 5/4
        pX1 = playerPosition[0] + changeX * paddingValue - playerWidth // 2
        pX2 = playerPosition[0] + changeX * paddingValue + playerWidth // 2
        pY1 = playerPosition[1] - changeY * paddingValue - playerHeight // 2
        pY2 = playerPosition[1] - changeY * paddingValue + playerHeight // 2

        for obj in self.structures:
            objectPosition = obj.getPosition()
            objectWidth, objectHeight = obj.getRect()[2:4]
            if obj.getCornerType == False:
                oX1 = objectPosition[0] - objectWidth // 2 + objectWiggleRoom
                oX2 = objectPosition[0] + objectWidth // 2 - objectWiggleRoom
                oY1 = objectPosition[1] - objectHeight // 2 + objectWiggleRoom
                oY2 = objectPosition[1] + objectHeight // 2 - objectWiggleRoom

                if (pX1 < oX2 and pX2 > oX1 and pY1 < oY2 and pY2 > oY1):
                    return True
            else:
                oX1 = objectPosition[0] + objectWiggleRoom
                oX2 = objectPosition[0] + objectWidth - objectWiggleRoom
                oY1 = objectPosition[1] + objectWiggleRoom
                oY2 = objectPosition[1] + objectHeight - objectWiggleRoom

                if (pX1 < oX2 and pX2 > oX1 and pY1 < oY2 and pY2 > oY1):
                    return True

        return False
