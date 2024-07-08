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


class Wire:

    wireAssets = {
        (3, 2) : "3-2-wire.png",
        (2, 1) : "2-1-wire.png",
        (3, 4) : "3-4-wire.png",
        (3, 1) : "3-1-wire.png",
        (4, 1) : "4-1-wire.png",
        (2, 4) : "2-4-wire.png"
    }
    '''  2
      3  +  1
         4
    '''
    def __init__(self, initialDirection = 3, finalDirection = 1, leftTile = None, rightTile = None,
                 bottomTile = None, upTile = None):
        self.type = (initialDirection, finalDirection)

        if initialDirection == 1:
            raise Exception()

        if initialDirection == 2:
            print()






