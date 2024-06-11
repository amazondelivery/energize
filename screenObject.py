import pygame as pg

class Object():

    screen_width = 1280
    screen_height = 720

    def renderText(self, font, text, antialias, color):
        return font.render(text, antialias, color)

    def renderImage(self, fileName):
        return pg.image.load(fileName)

    def renderImage(self, filename, transformation = False):
        if transformation == False:
            return pg.image.load(filename)
        else:
            image = pg.image.load(filename)
            return pg.transform.scale(image, transformation)

    def mids(self):
        return (self.screen_width / 2 - self.obj.get_width() // 2, self.screen_height / 2 - self.obj.get_height() // 2)

    def mid_height(self):
        return self.mids()[1]

    def mid_width(self):
        return self.mids()[0]

    def blit(self, offset = (0,0)):
        positionArray = self.position.copy()
        positionArray[0] += offset[0]
        positionArray[1] += offset[1]
        return self.obj, positionArray

    def getRect(self):
        return self.obj.get_rect()

    def regPosition(self, positionTuple):
        pos = [0,0]

        if positionTuple[0] == True:
            pos[0] = self.mid_width() + positionTuple[1]
        else:
            pos[0] = positionTuple[1]

        if positionTuple[2] == True:
            pos[1] = self.mid_height() - positionTuple[3]
        else:
            pos[1] = positionTuple[3]

        return pos


class Text(Object):
    def __init__(self, font, text, clickAction, color = pg.Color(255, 255, 255), position = (True, 0, True, 0), antialias = True):
        self.obj = self.renderText(font, text, antialias, color)
        self.clickAction = clickAction
        self.position = self.regPosition(position)

    def getAction(self):
        return self.clickAction

    def getPos(self):
        return self.position

class Image(Object):
    def __init__(self, imageName, clickAction, position = (True, 0, True, 0), transformation = None):
        if transformation == None:
            self.obj = self.renderImage(imageName)
        else:
            self.obj = self.renderImage(imageName, transformation)
        self.clickAction = clickAction
        self.position = self.regPosition(position)

    def getAction(self):
        return self.clickAction

    def getPos(self):
        return self.position

    def getRect(self):
        return self.obj.get_rect()

    def getX(self):
        return self.position[0]

    def getY(self):
        return self.position[1]

    def updatePos(self, x, y):
        self.position[0] += x
        self.position[1] -= y

    def instatePos(self, x, y):
        self.position[0] = x
        self.position[1] = y

class GameImage:
    def __init__(self, image, universalPosition, show = False):
        self.image = image
        self.universalPosition = universalPosition
        self.show = show

    def toggleShow(self):
        if self.show == True:
            self.show = False
        else:
            self.show = True

    def updateUniversalPosition(self, x, y):
        #error detection system goes here
        self.universalPosition[0] += x
        self.universalPosition[1] += y

