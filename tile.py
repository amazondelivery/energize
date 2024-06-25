class Tile:

    def __init__(self):
        self.type = 0
        self.lightLevel = 10

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


class Wire:

    def __init__(self, initialDirection, finalDirection = False):
        self.initialDirection = initialDirection
        self.finalDirection = finalDirection



