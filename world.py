from tile import Tile, TileMap
from structure import Structure, AnimatedStructure, Wire
from camera import *
from gradient import *
from timeController import TimeController
from inventory import Inventory
from utils import *
from asset import Map
from character import Player
import queue
import math
# at some point i want the world to be randomly generated with a seed

# i want to make the World class a lot smaller than it currently is. theres just way too much bloat i have to sort
# through every time i want to make changes

class World:

    tileDim = 80
    gradients = GameGradients()
    structureCode = BidirectionalDict({
            0 : "none",
            1 : "solar",
            2 : "wire",
            3 : "wind",
            4 : "windHelper",
            5 : "transformer"
        })
    initialCameraPoint = (640, 360)

    def __init__(self, screenDimensions):
        # making camera and gradients
        self.map_width, self.map_height = screenDimensions[0] * 4, screenDimensions[0] * 4
        self.screen_width, self.screen_height = 1280, 720
        self.camera = Camera((self.map_width, self.map_height), self.initialCameraPoint)
        # self.cameraUpdateQueue = [queue.Queue(), queue.Queue()]

        # images that the tiles will use
        self.map = Map("assets/images/game_map.png", (self.map_width, self.map_height), (False, 0, False, 0))
        self.player = Player("assets/images/groo.jpg", -1, (72,69), map_dimensions=(self.map_width, self.map_height))
        self.timeController = TimeController()

        # creates tilemap of width // 40 and height // 40) and initializes structures from previous playthrough
        self.tileMap = TileMap(self.tileDim, self.map_width, self.map_height)
        self.structures = self.initializeTileWorldStructures()

        #player settings
        self.inventory = Inventory(0, self.structureCode, {
            0 : 999999,
            1 : 15,
            2 : 20
        })

        # testing
        self.numSolarPanels = 15
        self.initializeStructure(5, (2,2))

        self.previousMousePosition = False

    def getPlayer(self):
        return self.player

    def getTileDim(self):
        return self.tileDim

    def getActualCurrentSelection(self):
        return self.inventory.getCurrentSelection() % self.inventory.getLength()

    def getCurrentSelection(self):
        return self.inventory.getCurrentSelection()

    def initializeStructure(self, typeOfStructure, tileCoord):
        pixelCoord = self.getCoordsOfTile(*tileCoord)
        if self.structureCode.get(typeOfStructure) == 'transformer':
            structure = AnimatedStructure("transformer", -1,
                                            self.structureCode.get(typeOfStructure), (False, pixelCoord[0], False, pixelCoord[1]))
            self.placeStructure(structure, pixelCoord)

        if self.getTileOfTileCoord(tileCoord).place(typeOfStructure):
            return True
        else:
            return False


    def initializeTileWorldStructures(self):
        structures = []
        for rowNum, tileRow in enumerate(self.tileMap.getMap()):
            for columnNum, tile in enumerate(tileRow):
                if tile.getType() != 0:
                    tileCoords = self.getCoordsOfTile(columnNum, rowNum)
                    structures.append(self.initializeStructure(type, tileCoords))
        return structures

    def updatePlayer(self, changeX, changeY):
        if not self.checkCollision(changeX, changeY):
            self.player.updatePos(changeX, changeY)

    def renderTiles(self):
        for rowNum, tileRow in enumerate(self.tileMap.getMap()):
            for columnNum, tile in enumerate(tileRow):
                print('test')

    def checkCollision(self, playerChangeX, playerChangeY):
        if self.mapCollision(playerChangeX, playerChangeY) or self.objectCollision(playerChangeX, playerChangeY):
            return True
        else:
            return False

    def getPlayerTile(self):
        position = self.player.getUniversalPosition()
        return (self.getTileLocationOfCoord(position))

    def getCamera(self):
        return self.camera

    def updateSelectedItem(self, y):
        currentSelection = self.inventory.getCurrentSelection()
        size = self.inventory.getSize()
        if (currentSelection + y) % size != currentSelection % size:
            self.inventory.updateCurrentSelection((currentSelection + y) % size)

    def getSelectedItem(self):
        return self.currentSelection % self.inventory.getLength()

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
        if self.outOfMapBounds(mapCoords) or self.inPlayersWay(mapCoords):
            print("cant place that here")
            return False
        elif self.outOfPlayerRange(mapCoords):
            print("out of range")
            return False
        else:
            self.place(mapCoords)
            return True

    def place(self, mapCoords):
        objectPosition = self.normalizeTileCornerPosition(mapCoords)
        mapTile = self.getTileLocationOfCoord(mapCoords)
        if self.structureCode.get(self.getActualCurrentSelection()) == "solar" and self.numSolarPanels > 0 and self.tilePlace(mapTile, self.getActualCurrentSelection()):
            structure = Structure("assets/images/solarDay.png", -1, self.structureCode.get(self.getActualCurrentSelection()), (False, objectPosition[0], False, objectPosition[1]))
            self.placeStructure(structure, mapCoords)
            self.solarPanelRemovalTestFunction()
        elif self.structureCode.get(self.getActualCurrentSelection()) == 'wire' and self.inventory.updateInventory(self.getActualCurrentSelection(), -1)\
            and self.tilePlace(mapTile, self.getActualCurrentSelection()):
            wire = Wire(objectPosition, 4, 2)
            self.placeStructure(wire, mapCoords)

    def solarPanelRemovalTestFunction(self):
        self.numSolarPanels -= 1
        print(self.numSolarPanels)

    def placeStructure(self, Structure, stickyMapCoords):
        self.structures.append(Structure)
        self.putStructureInTile(stickyMapCoords, Structure)

    def tilePlace(self, mapTile, type):
        if self.tileMap.getMap()[mapTile[1]][mapTile[0]].place(type) == True:
            return True
        else:
            return False

    def hover(self, frameCoords, mapCoords):
        if self.outOfMapBounds(mapCoords) or self.inPlayersWay(mapCoords):
            return False
        elif self.outOfPlayerRange(mapCoords):
            self.updateHoverTile(mapCoords)
            return False
        else:
            self.updateHoverTile(mapCoords)
            return True

    def updateHoverTile(self, mapCoords):
        if self.previousMousePosition != False:
            oldTile = self.previousMousePosition
            newTile = self.getTileLocationOfCoord(mapCoords)
            if oldTile != newTile:
                # print(f"new tile! because oldtile: {oldTile} and newTile: {newTile}") # test
                self.hideCaptionOfTile(oldTile)
                self.showCaptionOfTile(newTile)
                self.previousMousePosition = newTile
        else:
            self.previousMousePosition = self.getTileLocationOfCoord(mapCoords)

    def hideCaptionOfTile(self, tileLocation):
        tile = self.getTileOfTileCoord(tileLocation)
        if tile.containsStructure():
            tile.hideStructureCaption()

    def showCaptionOfTile(self, tileLocation):
        tile = self.getTileOfTileCoord(tileLocation)
        if tile.containsStructure():
            tile.showStructureCaption()

    def getCameraOffset(self):
        self.storedOffset = self.camera.getPlayerOffset(self.player.getPosition())
        return self.storedOffset

    def getTileOfCoord(self, mapCoords):
        location = self.getTileLocationOfCoord(mapCoords)
        return self.tileMap.getMap()[location[1]][location[0]]

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

    def getTileOfTileCoord(self, tileCoord):
        return self.tileMap.getMap()[tileCoord[1]][tileCoord[0]]

    def outOfMapBounds(self, mapCoords):
        x = mapCoords[0]
        y = mapCoords[1]

        if (x < 0 or x > self.map_width or y < 0 or y > self.map_height):
            return True
        else:
            return False

    def outOfPlayerRange(self, mapCoords):
        playerCoords = self.player.getUniversalPosition()
        if (math.sqrt((mapCoords[0] - playerCoords[0])**2 + (mapCoords[1] - playerCoords[1])**2)) > self.player.getRange():
            return True
        else:
            return False

    def mapCollision(self, changeX, changeY):
        playerRect = self.player.getRect()
        if changeX == 0:
            newY = self.player.getPosition()[1] - changeY
            if (newY - playerRect[3] // 2 < 0 or newY + playerRect[3] // 2 > self.map_height):
                return True
        else:
            newX = self.player.getPosition()[0] + changeX
            if (newX - playerRect[2] // 2 < 0 or newX + playerRect[2] // 2 > self.map_width):
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
        pY1 = playerPosition[1] - playerHeight // 2
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

    def updateCamera(self):
        mapFocus = self.map.getPosition().copy()
        mapFocus[0] += self.screen_width // 2
        mapFocus[1] += self.screen_height // 2
        self.camera.updateTruePosition(mapFocus)

    def putStructureInTile(self, tileCoord, Structure):
        tile = self.getTileOfCoord(tileCoord)
        tile.updateStructureReference(Structure)

    def normalizeTileCornerPosition(self, mapCoords):
        mapTile = self.getTileLocationOfCoord(mapCoords)
        return self.getCoordsOfTile(*mapTile)

    def objectCollision(self, changeX, changeY):
        # https://silentmatt.com/rectangle-intersection/
        # used the above link to help
        playerPosition = self.player.getPosition()
        objectWiggleRoom = 0  # probably not needed
        playerWidth, playerHeight = self.player.getRect()[2:4]
        pX1 = playerPosition[0] + changeX - playerWidth // 2
        pX2 = playerPosition[0] + changeX + playerWidth // 2
        pY1 = playerPosition[1] - changeY - playerHeight // 2
        pY2 = playerPosition[1] - changeY + playerHeight // 2

        for obj in self.structures:
            if obj.getWire() == True:
                continue
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

    def getMap(self):
        return self.map
