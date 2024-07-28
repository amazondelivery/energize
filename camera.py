import math
import queue


class Camera():

    def __init__(self, mapDimensions, initialFocus, initialPlayerPosition = (0,0)):
        self.mapDimensions = mapDimensions
        self.focus = [*initialFocus]

        self.previousPlayerPosition = [*initialPlayerPosition]

    def getPlayerOffset(self, playerPosition):
        # self.previousPlayerPosition = playerPosition
        return ((self.focus[0] - playerPosition[0]), (self.focus[1] - playerPosition[1]))


