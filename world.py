class Plot:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.color = "GREEN"

        def getCoords(self):
            return (self.x,self.y)

        def getX(self):
            return self.x

        def getY(self):
            return self.y

        def getColor(self):
            return self.color

        def setColor(self, color):
            self.color = color

        #for debug purposes
        def printThings(self):
            return f"({self.x}, {self.y})"
class World:

    def __init__(self):
        self.plots = []
        for y in range(64):
            row = []
            for x in range(64):
                row.append(Plot(x, y))
            self.plots.append(row)
        print(self.plots)

    def returnPlot(self):
        return self.plots

    class WorldBuilder:
        def __init__(self):
            print("to be completed later")


