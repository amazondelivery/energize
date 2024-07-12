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








