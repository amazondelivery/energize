from gameStructure.asset import Image, Text, renderText
import pygame as pg

class GUI(Image):
    def __init__(self, imageName, left, top, transformation = None, show = True, transparent = True, clickAction = -1):

        self.transparent = transparent
        self.obj = self.transformationChecker(imageName, transformation)
        self.rect = self.getRect()
        self.clickAction = clickAction
        self.position = self.regPosition(left, top)
        self.cornerPlace = True
        self.show = show

    def regPosition(self, left, top):
        width, height = self.getWidthHeight()
        if left < 0:
            x = self.screen_width + left - width
            # right side must be -left from the right side of the screen
        else:
            x = left
            # left side must be left from the left side of the screen

        if top < 0:
            # bottom side must be -top from the bottom side of the screen
            y = self.screen_height + top - height
        else:
            y = top
            # top side must be top from the top side of the screen

        return (x, y)

    def blit(self):
        width, height = self.getWidthHeight()
        positionArray = self.position

        #remove the width and height adjustments after positionArrays are normalized to be in the middle
        if not self.cornerPlace:
            positionArray[0] = positionArray[0] - width // 2
            positionArray[1] = positionArray[1] - height // 2
            return self.obj, positionArray
        else:
            return self.obj, positionArray

class NumberGUI(Text):
    def __init__(self, initialNumber, left, top, font, color = pg.Color(255, 255, 255), antialias = True,
                 transformation = None, show = True, transparent = True, clickAction = -1):

        self.obj = renderText(font, str(initialNumber), color, antialias)
        self.rect = self.obj.get_rect()
        self.transparent = transparent
        self.counter = initialNumber
        self.font = font
        self.color = color
        self.antialias = antialias
        self.position = self.regPosition(left, top)
        self.cornerPlace = True
        self.show = show


    def update(self, byHowMuch):
        self.counter += byHowMuch
        self.rerender(str(self.counter))

    def rerender(self, newText):
        self.obj = renderText(self.font, newText, self.color, self.antialias)

    def regPosition(self, left, top):
        width, height = self.getWidthHeight()
        if left < 0:
            x = self.screen_width + left - width
            # right side must be -left from the right side of the screen
        else:
            x = left
            # left side must be left from the left side of the screen

        if top < 0:
            # bottom side must be -top from the bottom side of the screen
            y = self.screen_height + top - height
        else:
            y = top
            # top side must be top from the top side of the screen

        return (x, y)


# basic GUI that encompasses a number
# backgroundGUI is an additional GUI object that is the background of the number
class ScoreTicker(GUI):
    def __init__(self, backgroundGUI, left, top, initialNumber, font,
                 unitsAsString, textColor=pg.Color("White"), clickAction=-1):
        self.number = initialNumber
        self.string = unitsAsString
        self.clickAction = clickAction

        self.position = self.regPosition(left, top)
        self.textColor = textColor
        self.backgroundGUI = backgroundGUI
        self.font = font
        self.text = Text(font, str(self.number) + self.string, textColor,
                         self.position, cornerPlace=True)

    def getNumber(self):
        return self.number

    def setNumber(self, newNumber):
        self.number = newNumber
        self.text = Text(self.font, str(self.number) + self.string, self.textColor,
                         self.position, cornerPlace=True)






