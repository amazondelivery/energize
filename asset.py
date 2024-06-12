#may eventually want this class to replace screenObject, because i want a universal position format
import pygame as pg

class Asset:

    screen_width = 1280
    screen_height = 720

    def renderText(self, font, text, color, antialias = True):
        font.render(text, antialias, color)

    def getAction(self):
        return self.clickAction

    def renderImage(self, filename, transformation = False):
        if transformation == False:
            return pg.image.load(filename)
        else:
            image = pg.image.load(filename)
            return pg.transform.scale(image, transformation)

    def mids(self):
        return (self.screen_width // 2, self.screen_height // 2)

    def midWidth(self):
        return self.mids(self.screen_width, self.screen_height)[0]

    def midHeight(self):
        return self.mids(self.screen_width, self.screen_height)[1]

    def blit(self, offset = (0,0)):
        width, height = self.getWidthHeight()
        positionArray = self.position.copy()

        #remove the width and height adjustments after positionArrays are normalized to be in the middle
        positionArray[0] = positionArray[0] + offset[0] - width//2
        positionArray[1] = positionArray[1] + offset[1] - height // 2
        return self.obj, positionArray

    def getWidthHeight(self):
        rect = self.getRect()
        return (rect[2], rect[3])

    def getRect(self):
        return self.obj.get_rect()

    def getPosition(self):
        return self.position

    def updatePosition(self, x, y):
        self.position[0] += x
        self.position[1] -= y

    def forcePosition(self, x, y):
        #forces a position, not recommended to use
        self.position[0] = x
        self.position[0] = y

    def regPosition(self, positionTuple):
        mid_width, mid_height = self.mids()
        pos = [0,0]

        if positionTuple[0] == True:
            pos[0] = mid_width + positionTuple[1]
        else:
            pos[0] = positionTuple[1]

        if positionTuple[2] == True:
            pos[1] = mid_height - positionTuple[3]
        else:
            pos[1] = positionTuple[3]

        return pos

    def getCornerPosition(self, ):
        if self.cornerPlace == True:
            raise Exception("Just getPosition() next time man")
        else:
            position = self.position.copy()
            width, height = self.getWidthHeight()
            position[0] -= width // 2
            position[1] -= height // 2
        return position

class Text(Asset):
    def __init__(self, font, text, clickAction, color = pg.Color(255, 255, 255),
                 position = (True, 0, True, 0), antialias = True, cornerPlace = False):
        self.obj = self.renderText(font, text, color, antialias)
        self.clickAction = clickAction
        self.position = self.regPosition(position)
        self.cornerPlace = cornerPlace

class Image(Asset):
    def __init__(self, imageName, clickAction,
                 position = (True, 0, True, 0), transformation = None, cornerPlace = False):
        if transformation == None:
            self.obj = self.renderImage(imageName)
        else:
            self.obj = self.renderImage(imageName, transformation)
        self.clickAction = clickAction
        self.position = self.regPosition(position)
        self.cornerPlace = cornerPlace


