# class idea and __setitem__ and __del__item borrowed from https://stackoverflow.com/a/1063393
class BidirectionalDict(dict):
    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        dict.__setitem__(self, val, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

class Calculations:

    # will move collision functions and distance calculations here eventually
    def nothing(self):
        print()
