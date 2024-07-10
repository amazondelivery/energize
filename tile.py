from structure import Structure, AnimatedStructure

class TileMap:
    def __init__(self, tileDim, map_width, map_height):
        self.tileMap = [[Tile() for i in range(map_width // tileDim)] for j in range(map_height // tileDim)]
        self.tileDim = tileDim
        self.map_width, self.map_height = map_width, map_height

    def getMap(self):
        return self.tileMap

    def getTileDim(self):
        return self.tileDim

    def getMapWidth(self):
        return self.map_width

    def getMapHeight(self):
        return self.map_height




class Tile:

    def __init__(self):
        self.type = 0
        self.lightLevel = 10

        # i want the tile object to hold a reference to the structure because itll make it easier to access
        # a tile's structure
        self.structureRef = None
        self.wire = None

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

    def getType(self):
        return self.type

    def updateStructureReference(self, Structure):
        # rare uppercase variable! oooo
        self.structureRef = Structure

    def getStructureReference(self):
        return self.structureRef

    def hideStructureCaption(self):
        self.structureRef.hideCaption()

    def showStructureCaption(self):
        self.structureRef.showCaption()

    def containsStructure(self):
        if self.structureRef == None:
            return False
        else:
            return True

    def getWire(self):
        return self.wire

    def setWire(self, Wire):
        self.wire = Wire


class Wire:

    wireAssets = {
        (3, 2) : "3-2-wire.png",
        (2, 3) : "3-2-wire.png",
        (2, 1) : "2-1-wire.png",
        (1, 2): "2-1-wire.png",
        (3, 4) : "3-4-wire.png",
        (4, 3): "3-4-wire.png",
        (3, 1) : "3-1-wire.png",
        (1, 3): "3-1-wire.png",
        (4, 1) : "4-1-wire.png",
        (1, 4): "4-1-wire.png",
        (2, 4) : "2-4-wire.png",
        (4, 2): "2-4-wire.png"
    }
    '''  2
      3  +  1
         4
    '''
    def __init__(self, pixelCornerPosition, initialDirection = 3, finalDirection = 1, leftTile = None, rightTile = None,
                 bottomTile = None, upTile = None):
        self.type = (initialDirection, finalDirection)

        self.wireStructure = Structure(
            f"assets/images/wire/{self.wireAssets[(initialDirection, finalDirection)]}.png",
            -1, "Wire", position=(False, pixelCornerPosition[0], False, pixelCornerPosition[1]),
        )
        self.prev = None
        self.next = None

        if initialDirection == 1:
            self.prev = rightTile
        elif initialDirection == 2:
            self.prev = upTile
        elif initialDirection == 3:
            self.prev = leftTile
        elif initialDirection == 4:
            self.prev = bottomTile
        else:
            raise Exception()

        if finalDirection == 1:
            self.next = rightTile
        elif finalDirection == 2:
            self.next = upTile
        elif finalDirection == 3:
            self.next = leftTile
        elif finalDirection == 4:
            self.next = bottomTile
        else:
            raise Exception()








