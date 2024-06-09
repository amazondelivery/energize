class Gradient:

    def __init__(self, colors, timeStop):
        self.numStops = len(colors)
        self.colors = colors
        self.timeStop = timeStop

    def getTimeStop(self):
        return self.timeStop

    def getColor(self, inc):
        return self.colors[inc]

    def getNumStops(self):
        return self.numStops

class GameGradients:
    #includes all the gradients used in the game backgrounds
    def __init__(self):
        self.gradients = {
            "sunset" :
            Gradient(
            ((6, 4, 4),
            (8, 10, 10),
            (10, 15, 16),
            (13, 20, 23),
            (15, 26, 29),
            (17, 32, 35),
            (19, 37, 41),
            (22, 43, 48),
            (24, 48, 54),
            (26, 54, 60),
            (28, 59, 66),
            (30, 65, 72),
            (33, 70, 79),
            (35, 76, 85),
            (37, 81, 91),
            (39, 87, 97),
            (42, 92, 103),
            (44, 98, 110),
            (46, 103, 116),
            (48, 109, 122),
            (50, 114, 128),
            (53, 120, 135),
            (55, 125, 141),
            (57, 131, 147),
            (59, 136, 153),
            (61, 142, 159),
            (64, 147, 166),
            (66, 153, 172),
            (68, 158, 178),
            (70, 163, 184),
            (73, 169, 191),
            (75, 175, 197),
            (77, 180, 203)),
            5)
        }

    def getGradient(self, name):
        return self.gradients[name]
