#at some point i want the world to be randomly generated with a seed
from tile import Tile
from screenObject import Image

class World:
    def __init__(self, mapDimensions = (0, 0)):

        #error-checking
        if mapDimensions[0] == 0 or mapDimensions[1] == 0:
            raise NotImplementedError

        #images that the tiles will use
        assets = {
           #"solarDay" : Image("solarDay.png", -1)
        }

        self.day = True

        #creates tilemap of width // 40 and height // 40)
        self.tileMap = [ [Tile()] * (mapDimensions[1] // 40) for i in range(mapDimensions[0] // 40) ]

        self.mapDimensions = mapDimensions


