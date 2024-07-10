class Inventory:

    def __init__(self, startingValue, codeBook, startingInventory):
        self.codeBook = codeBook
        self.inventory = startingInventory
        self.currentSelection = startingValue

    def getLength(self):
        return len(self.inventory)

    def updateCurrentSelection(self, currentSelection):
        self.currentSelection = currentSelection

    def getCurrentSelection(self):
        return self.currentSelection

    def getSize(self):
        return len(self.inventory)

    def updateInventory(self, code, num):
        if self.inventory[code] > 0:
            return False
        self.inventory[code] += num
        return True
