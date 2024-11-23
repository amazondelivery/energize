from tile import Map
from gameStructure.structure import Structure, AnimatedStructure, Wire
from gameStructure.camera import *
from gameStructure.gradient import *
from gameStructure.timeController import TimeController
from gameStructure.inventory import Inventory
from utils import *
from gameStructure.character import Player
import queue
import math
# at some point i want the world to be randomly generated with a seed


class World:

    objectWiggleRoom = 0  # should probably stay 0
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
    tileDim = 80

    def __init__(self, screenDimensions):
        # map and screens widths and heights
        self.map_width, self.map_height = screenDimensions[0] * 4, screenDimensions[0] * 4
        self.screen_width, self.screen_height = screenDimensions[0], screenDimensions[1]
        self.camera = Camera((self.map_width, self.map_height), self.initialCameraPoint)

        # map, player, time controller
        playerConversionFactor = 2.5
        self.map = Map("assets/images/maps/game_map1.png", (self.map_width, self.map_height), self.tileDim)
        self.player = Player("assets/images/player", (round(39 * playerConversionFactor), round(77 * playerConversionFactor)), map_dimensions=(self.map_width, self.map_height))
        self.timeController = TimeController()
        self.structures = self.initializeTileWorldStructures()

        #player settings
        self.inventory = Inventory(0, self.structureCode, {
            0 : 999999,
            1 : 15,
            2 : 20
        })

        # default Structures
        self.initializeStructure(5, (2,2))

        self.previousMousePosition = False

    def getPlayer(self):
        return self.player

    def getTileDim(self):
        return self.tileDim

    def getCurrentSelection(self):
        return self.inventory.getCurrentSelection() % self.inventory.getLength()

    def initializeStructure(self, typeOfStructure, tileCoord):
        pixelCoord = self.map.getCoordsOfTile(*tileCoord)
        if self.structureCode.get(typeOfStructure) == 'transformer':
            structure = AnimatedStructure("transformer",
                                          self.structureCode.get(typeOfStructure), (False, pixelCoord[0], False, pixelCoord[1]))
            self.placeStructure(structure, pixelCoord)

        if self.map.getTileOfTileCoord(tileCoord).place(typeOfStructure):
            return True
        else:
            return False

    def initializeTileWorldStructures(self):
        structures = []
        for rowNum, tileRow in enumerate(self.map.getTileMap()):
            for columnNum, tile in enumerate(tileRow):
                if tile.getType() != 0:
                    tileCoords = self.getCoordsOfTile(columnNum, rowNum)
                    structures.append(self.initializeStructure(type, tileCoords))
        return structures

    def updatePlayer(self, changeX, changeY):
        if not self.checkCollision(changeX, changeY):
            self.player.updatePos(changeX, changeY)

    def renderTiles(self):
        for rowNum, tileRow in enumerate(self.map.getTileMap()):
            for columnNum, tile in enumerate(tileRow):
                print('test')

    def checkCollision(self, playerChangeX, playerChangeY):
        if self.mapCollision(playerChangeX, playerChangeY) or self.objectCollision(playerChangeX, playerChangeY):
            return True
        else:
            return False

    def getPlayerTile(self):
        position = self.player.getUniversalPosition()
        return (self.map.getTileLocationOfCoord(position))

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
        newTime = self.timeController.timeIncrease()


    def place(self, mapCoords):
        objectPosition = self.map.normalizeTileCornerPosition(mapCoords)
        mapTile = self.map.getTileLocationOfCoord(mapCoords)
        currentSelection = self.getCurrentSelection()
        if self.map.getTileOfCoord(mapCoords).getType() == 2:
            self.map.getTileOfCoord(mapCoords).getStructureReference().update()
        elif self.structureCode.get(currentSelection) == "solar" and self.map.tilePlace(mapTile, currentSelection)\
                and self.inventory.updateInventory(currentSelection, -1):
            structure = Structure("assets/images/solarDay.png", self.structureCode.get(currentSelection),
                                  (False, objectPosition[0], False, objectPosition[1]))
            self.placeStructure(structure, mapCoords)
        elif self.structureCode.get(self.getCurrentSelection()) == 'wire' and self.inventory.updateInventory(self.getCurrentSelection(), -1)\
            and self.map.tilePlace(mapTile, self.getCurrentSelection()):
            wire = Wire(objectPosition, 4, 2)
            self.placeStructure(wire, mapCoords)

    def placeStructure(self, Structure, stickyMapCoords):
        self.structures.append(Structure)
        self.map.putStructureInTile(stickyMapCoords, Structure)

    def hover(self, frameCoords, mapCoords):
        if self.map.outOfMapBounds(mapCoords) or self.inPlayersWay(mapCoords):
            return False
        elif self.outOfPlayerRange(mapCoords):
            self.updateHoverTile(mapCoords, frameCoords)
            return False
        else:
            self.updateHoverTile(mapCoords, frameCoords)
            return True

    def updateHoverTile(self, mapCoords, frameCoords):
        if self.previousMousePosition != False:
            oldTile = self.previousMousePosition
            newTile = self.map.getTileLocationOfCoord(mapCoords)
            if oldTile != newTile:

                # Hides caption of old tile
                tile = self.map.getTileOfTileCoord(oldTile)
                if tile.containsStructure():
                    tile.hideCaption()

                # Shows caption of new tile
                tile = self.map.getTileOfTileCoord(newTile)
                if tile.containsStructure():
                    tile.showCaption()

                self.previousMousePosition = newTile
        else:
            self.previousMousePosition = self.map.getTileLocationOfCoord(mapCoords)

    def getCameraOffset(self):
        self.storedOffset = self.camera.getPlayerOffset(self.player.getPosition())
        return self.storedOffset

    def getLocationOfTile(self, tile):
        # not a very efficient function so prefer not to use
        for rowNum, tileRow in enumerate(self.map.getTileMap()):
            for columnNum, tileIterate in enumerate(tileRow):
                if tile == tileIterate:
                    return (columnNum, rowNum)

    def outOfPlayerRange(self, mapCoords):
        playerCoords = self.player.getUniversalPosition()
        if (math.sqrt((mapCoords[0] - playerCoords[0])**2 + (mapCoords[1] - playerCoords[1])**2)) > self.player.getRange():
            return True
        else:
            return False

    def inPlayersWay(self, mapCoords):
        mapTile = self.map.getTileLocationOfCoord(mapCoords)
        playerTile = self.getPlayerTile()
        if mapTile[0] == playerTile[0] and mapTile[1] == playerTile[1]:
            return True

        playerPosition = self.player.getUniversalPosition()
        playerWidth, playerHeight = self.player.getRect()[2:4]
        pX1 = playerPosition[0] - playerWidth // 2
        pX2 = playerPosition[0] + playerWidth // 2
        pY1 = playerPosition[1] - playerHeight // 2
        pY2 = playerPosition[1] + playerHeight // 2

        objectPosition = self.map.getCoordsOfTile(*mapTile)
        oX1 = objectPosition[0]
        oX2 = objectPosition[0] + self.tileDim
        oY1 = objectPosition[1]
        oY2 = objectPosition[1] + self.tileDim

        if (pX1 < oX2 and pX2 > oX1 and pY1 < oY2 and pY2 > oY1):
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

    def objectCollision(self, changeX, changeY):
        # https://silentmatt.com/rectangle-intersection/
        # used the above link to help
        playerPosition = self.player.getPosition()
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
                oX1 = objectPosition[0] - objectWidth // 2 + self.objectWiggleRoom
                oX2 = objectPosition[0] + objectWidth // 2 - self.objectWiggleRoom
                oY1 = objectPosition[1] - objectHeight // 2 + self.objectWiggleRoom
                oY2 = objectPosition[1] + objectHeight // 2 - self.objectWiggleRoom

                if (pX1 < oX2 and pX2 > oX1 and pY1 < oY2 and pY2 > oY1):
                    return True
            else:
                oX1 = objectPosition[0] + self.objectWiggleRoom
                oX2 = objectPosition[0] + objectWidth - self.objectWiggleRoom
                oY1 = objectPosition[1] + self.objectWiggleRoom
                oY2 = objectPosition[1] + objectHeight - self.objectWiggleRoom

                if (pX1 < oX2 and pX2 > oX1 and pY1 < oY2 and pY2 > oY1):
                    return True

        return False

    def getMap(self):
        return self.map
