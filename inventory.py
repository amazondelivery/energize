class Inventory:

    def __init__(self, startingValue, codeBook, startingInventory):
        self.codeBook = codeBook
        self.startingInventory = startingInventory
        self.currentSelection = startingValue

    def getLength(self):
        return len(self.startingInventory)

    def updateCurrentSelection(self, currentSelection):
        self.currentSelection = currentSelection

    def getCurrentSelection(self):
        return self.currentSelection
