class TimeController:

    def __init__(self):
        self.day = True
        self.time = 0

    def timeIncrease(self):
        self.time += 1

    def getTime(self):
        return self.time
