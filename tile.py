from gameStructure.structure import Structure, AnimatedStructure
from gameStructure.asset import Asset


class Map(Asset):

    def __init__(self, imageName, transformation, tileDim, position = (False, 0, False, 0)):
        self.transparent = False
        self.obj = self.renderImage(imageName, transformation)
        self.clickAction = -1
        self.position = self.regPosition(position)
        self.universalCornerPosition = [0,0]
        self.rect = self.getRect()

        map_width, map_height = transformation
        self.tileMap = [[Tile() for i in range(map_width // tileDim)] for j in range(map_height // tileDim)]
        self.tileDim = tileDim
        self.map_width, self.map_height = map_width, map_height

    def blit(self, offset = (0,0)):
        positionArray = self.position.copy()
        positionArray[0] += offset[0]
        positionArray[1] += offset[1]
        self.universalCornerPosition[0], self.universalCornerPosition[1] = -positionArray[0], -positionArray[1]
        return self.obj, positionArray

    def getUniversalCornerPosition(self):
        return self.universalCornerPosition.copy()
    
    def getTileMap(self):
        return self.tileMap

    def getTileDim(self):
        return self.tileDim

    def getMapWidth(self):
        return self.map_width

    def getMapHeight(self):
        return self.map_height

    def loadSavedStructures(self):
        structures = []
        for rowNum, tileRow in enumerate(self.map.getTileMap()):
            for columnNum, tile in enumerate(tileRow):
                if tile.getType() != 0:
                    tileCoords = self.getCoordsOfTile(columnNum, rowNum)
                    structures.append(self.initializeStructure(type, tileCoords))
        return structures

    def getTileLocationOfCoord(self, mapCoords):
        return (mapCoords[0] // self.tileDim, mapCoords[1] // self.tileDim)

    def getTileOfCoord(self, mapCoords):
        location = self.getTileLocationOfCoord(mapCoords)
        return self.tileMap[location[1]][location[0]]

    def getTileOfTileCoord(self, tileCoord):
        return self.tileMap[tileCoord[1]][tileCoord[0]]

    def getCoordsOfTile(self, col, row):
        return (col * self.tileDim, row * self.tileDim)

    def tilePlace(self, mapTile, type):
        if self.tileMap[mapTile[1]][mapTile[0]].place(type) == True:
            return True
        else:
            return False

    def normalizeTileCornerPosition(self, mapCoords):
        mapTile = self.getTileLocationOfCoord(mapCoords)
        return self.getCoordsOfTile(*mapTile)

    def putStructureInTile(self, tileCoord, Structure):
        tile = self.getTileOfCoord(tileCoord)
        tile.updateStructureReference(Structure)

    def outOfMapBounds(self, mapCoords):
        x = mapCoords[0]
        y = mapCoords[1]

        if (x < 0 or x > self.map_width or y < 0 or y > self.map_height):
            return True
        else:
            return False


class Tile:

    def __init__(self):
        self.type = 0
        self.lightLevel = 10

        # i want the tile object to hold a reference to the structure because itll make it easier to access
        # a tile's structure
        self.structureRef = None
        self.parentCluster = None

    def place(self, type):
        if self.isEmpty():
            self.type = type

            return True
        else:
            return False

    def isEmpty(self):
        if self.type == 0:
            return True
        else:
            print(self.type)
            return False

    def isEqual(self, type):
        if self.type == type:
            return True
        else:
            return False

    def getType(self):
        return self.type

    def updateStructureReference(self, Structure):
        # rare uppercase variable! oooo
        self.structureRef = Structure

    def getStructureReference(self):
        return self.structureRef

    def hideCaption(self):
        self.structureRef.hideCaption()

    def showCaption(self):
        self.structureRef.showCaption()

    def containsStructure(self):
        if self.structureRef == None:
            return False
        else:
            return True

    def getCluster(self):
        return self.parentCluster

    def setCluster(self, cluster):
        self.parentCluster = cluster


def getSurroundingClusters(tileLocation, tileMap, type):

    #      1
    #  2   +   0
    #      3
    clusters = [None, None, None, None]

    if tileLocation[0] > 0 and tileMap[tileLocation[1]][tileLocation[0] - 1].isEqual(type):
            clusters[2] = tileMap[tileLocation[1]][tileLocation[0] - 1].getCluster()

    if tileLocation[1] > 0 and tileMap[tileLocation[1] - 1][tileLocation[0]].isEqual(type):
            clusters[1] = tileMap[tileLocation[1]][tileLocation[0] - 1].getCluster()

    if tileLocation[0] < len(tileMap[0]) - 1 and tileMap[tileLocation[1]][tileLocation[0] + 1].isEqual(type):
            clusters[0] = tileMap[tileLocation[1]][tileLocation[0] - 1].getCluster()

    if tileLocation[1] < len(tileMap) - 1 and tileMap[tileLocation[1] + 1][tileLocation[0]].isEqual(type):
            clusters[3] = tileMap[tileLocation[1]][tileLocation[0] - 1].getCluster()

    return clusters










