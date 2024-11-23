class TimeController:

    def __init__(self):
        self.time = 0

        # constants

    def timeIncrease(self, increment=1):
        self.time += increment
        return self.time

    def getTime(self):
        return self.time

    def isDayTime(self):
        # to be filled in
        return True
