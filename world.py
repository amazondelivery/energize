#at some point i want the world to be randomly generated with a seed
from tile import Tile
from screenObject import Image
from camera import *
from gradient import *
from player import Player
from timeController import TimeController

class World:
    def __init__(self, map, assets, player, mapDimensions = (0, 0), initialCameraPoint = (0,0)):

        #error-checking
        if mapDimensions[0] == 0 or mapDimensions[1] == 0:
            raise NotImplementedError

        #making camera and gradients
        map_width, map_height = mapDimensions
        self.camera = Camera((map_width, map_height), initialCameraPoint)
        self.gradients = GameGradients()

        #images that the tiles will use
        self.map = map
        self.assets = assets
        self.player = player
        self.timeController = TimeController()

        self.structures = [
            #test
            Image("solarBright.png", -1, (False, 900, False, 900), transformation = (80,80))
        ]

        #creates tilemap of width // 40 and height // 40)
        self.tileMap = [ [Tile()] * (mapDimensions[1] // 40) for i in range(mapDimensions[0] // 40) ]

        self.mapDimensions = mapDimensions

    def getPlayer(self):
        return self.player

    def updatePlayer(self, x, y):
        self.player.updatePos(x, y)

    def getMap(self):
        return self.map

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




