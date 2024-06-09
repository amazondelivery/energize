class Tile:

    def __init__(self):
        # random variable to give it some meaning to be a tile in existence
        self.type = 0
        self.lightLevel = 10

    def solarify(self):
        self.type == 1

    def windify(self):
        self.type == 2

    def windifyHelper(self):
        self.type == 3


class Wire:

    def __init__(self, initialDirection, finalDirection = False):
        self.initialDirection = initialDirection
        self.finalDirection = finalDirection



