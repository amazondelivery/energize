import pygame as pg


def renderText(font, text, color, antialias = True):
    return font.render(text, antialias, color)


class Asset:

    screen_width = 1280
    screen_height = 720
    tileDim = 80

    def getAction(self):
        return self.clickAction

    def renderImage(self, filename, transformation = False):
        if self.transparent == True:
            if transformation == False:
                return pg.image.load(filename)
            else:
                image = pg.image.load(filename)
                return pg.transform.scale(image, transformation)
        else:
            if transformation == False:
                return pg.image.load(filename).convert()
            else:
                image = pg.image.load(filename)
                return pg.transform.scale(image, transformation).convert()

    def mids(self):
        return (self.screen_width // 2, self.screen_height // 2)

    def midWidth(self):
        return self.mids(self.screen_width, self.screen_height)[0]

    def midHeight(self):
        return self.mids(self.screen_width, self.screen_height)[1]

    def getCornerType(self):
        return self.cornerPlace

    def blit(self, offset = (0,0)):
        width, height = self.getWidthHeight()
        if self.cornerPlace:
            return self.obj, [self.position[0] + offset[0], self.position[1] + offset[1]]
        else:
            return self.obj, [self.position[0] + offset[0] - width // 2, self.position[1] + offset[1] - height // 2]

    def getWidthHeight(self):
        return (self.rect[2], self.rect[3])

    def getRect(self):
        return self.obj.get_rect()

    def getPosition(self):
        return self.position

    def updatePosition(self, x, y):
        self.position[0] += x
        self.position[1] -= y

    def forcePosition(self, x, y):
        self.position[0] = x
        self.position[1] = y

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

    def showObject(self):
        self.show = True

    def showWithPosition(self, coords):
        self.forcePosition(coords[0], coords[1])
        self.showObject()

    def hideObject(self):
        self.show = False

    def getShow(self):
        return self.show

class Text(Asset):
    def __init__(self, font, text, color = pg.Color(255, 255, 255),
                 position = (True, 0, True, 0), antialias = True, cornerPlace = False, show = True,
                 clickAction = -1):
        self.obj = renderText(font, text, color, antialias)
        self.clickAction = clickAction
        self.position = self.regPosition(position)
        self.cornerPlace = cornerPlace
        self.show = show
        self.rect = self.getRect()
        self.transparent = True
        self.font = font
        self.color = color
        self.antialias = antialias


class Image(Asset):
    def __init__(self, imageName, position = (True, 0, True, 0), \
                 transformation = None, cornerPlace = False, show = True,
                 transparent = False, clickAction = -1, naturalPosition = None):

        self.transparent = transparent
        if transformation == None:
            self.obj = self.renderImage(imageName)
        else:
            self.obj = self.renderImage(imageName, transformation)
        self.clickAction = clickAction
        if naturalPosition == None:
            self.position = self.regPosition(position)
        else:
            self.position = naturalPosition
        self.cornerPlace = cornerPlace
        self.show = show
        self.rect = self.getRect()

    def transformationChecker(self, imageName, transformation):
        if transformation == None:
            return self.renderImage(imageName)
        else:
            return self.renderImage(imageName, transformation)




