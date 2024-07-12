from asset import Image, Text
import pygame as pg
from os import listdir

labelSize = 20
labelUpMove = 20
class Structure(Image):
    def __init__(self, imageName, clickAction, label,
                 position = (False, 0, False, 0), transformation = None, cornerPlace = True, show = True, wire = False):
        if transformation == None:
            self.obj = self.renderImage(imageName, (self.tileDim, self.tileDim))
        else:
            self.obj = self.renderImage(imageName, transformation)
        self.clickAction = clickAction
        self.position = self.regPosition(position)
        self.cornerPlace = cornerPlace
        self.show = show
        self.rect = self.getRect()
        self.isWire = wire
        self.label = self.initLabel(label)

    def blitLabel(self, offset):
        return self.label.blit(offset)

    def getBlitShow(self):
        return self.label.getShow()

    def showCaption(self):
        self.label.showObject()

    def hideCaption(self):
        self.label.hideObject()

    def getWire(self):
        return self.isWire

    def initLabel(self, label):
        font = pg.font.Font("assets/fonts/MajorMonoDisplay-Regular.ttf", labelSize)
        return Text(font, label, -1, pg.Color(255, 255, 255),
                          (False, self.position[0], False, self.position[1] - labelUpMove), show = False)

class AnimatedStructure(Structure):
    #this was kind of hard to figure out because at first i tried to make my overloaded blit() function would call
    #the parent Image class blit(), which i found out was very hard to do
    def __init__(self, imageFolder, clickAction, label, position = (False, 0, False, 0), transformation = None, cornerPlace = True, show = True,
                 startingFrame = 0, wire = False):
        self.objs = [self.renderImage(f"assets/images/{imageFolder}/{imageName}", (self.tileDim, self.tileDim))
                         for imageName in listdir(f"assets/images/{imageFolder}")]
        self.clickAction = clickAction
        self.position = self.regPosition(position)
        self.cornerPlace = cornerPlace
        self.show = show
        self.frame = startingFrame
        self.animationLength = len(self.objs)
        self.rect = self.getRect()
        self.isWire = wire
        self.label = self.initLabel(label)

    def blit(self, offset = (0,0)):
        obj = self.objs[self.frame]
        self.frame = (self.frame + 1) % self.animationLength
        width, height = self.getWidthHeight()
        if self.cornerPlace:
            return obj, [self.position[0] + offset[0], self.position[1] + offset[1]]
        else:
            return obj, [self.position[0] + offset[0] - width // 2, self.position[1] + offset[1] - height // 2]

    def getRect(self):
        return self.objs[0].get_rect()


class WireTest(Structure):

    wireAssets = {
        (3, 2) : "3-2-wire.png",
        (2, 3) : "3-2-wire.png",
        (2, 1) : "2-1-wire.png",
        (1, 2): "2-1-wire.png",
        (3, 4) : "3-4-wire.png",
        (4, 3): "3-4-wire.png",
        (3, 1) : "3-1-wire.png",
        (1, 3): "3-1-wire.png",
        (4, 1) : "4-1-wire.png",
        (1, 4): "4-1-wire.png",
        (2, 4) : "2-4-wire.png",
        (4, 2): "2-4-wire.png"
    }
    '''  2
      3  +  1
         4
    '''
    def __init__(self, pixelCornerPosition, initialDirection = 3, finalDirection = 1, leftTile = None, rightTile = None,
                 bottomTile = None, upTile = None):
        self.type = (initialDirection, finalDirection)

        self.wireStructure = Structure(
            f"assets/images/wire/{self.wireAssets[(initialDirection, finalDirection)]}.png",
            -1, "Wire", position=(False, pixelCornerPosition[0], False, pixelCornerPosition[1]), wire = True
        )
        self.prev = None
        self.next = None

        if initialDirection == 1:
            self.prev = rightTile
        elif initialDirection == 2:
            self.prev = upTile
        elif initialDirection == 3:
            self.prev = leftTile
        elif initialDirection == 4:
            self.prev = bottomTile
        else:
            raise Exception()

        if finalDirection == 1:
            self.next = rightTile
        elif finalDirection == 2:
            self.next = upTile
        elif finalDirection == 3:
            self.next = leftTile
        elif finalDirection == 4:
            self.next = bottomTile
        else:
            raise Exception()

    def __init__(self, pixelCornerPosition, initialDirection = 3, finalDirection = 1, leftTile = None, rightTile = None,
                 bottomTile = None, upTile = None):
        if transformation == None:
            self.objs = [self.renderImage(f"assets/images/{imageFolder}/{imageName}", (self.tileDim, self.tileDim))
                         for imageName in listdir(f"assets/images/{imageFolder}")]
        else:
            self.objs = [self.renderImage(f"assets/images/{imageFolder}/{imageName}", transformation)
                         for imageName in listdir(f"assets/images/{imageFolder}")]
        self.clickAction = clickAction
        self.position = self.regPosition(position)
        self.cornerPlace = cornerPlace
        self.show = show
        self.frame = startingFrame
        self.animationLength = len(self.objs)
        self.rect = self.getRect()
        self.isWire = wire
        self.label = self.initLabel(label)

    def blit(self, offset = (0,0)):
        obj = self.objs[self.frame]
        self.frame = (self.frame + 1) % self.animationLength
        width, height = self.getWidthHeight()
        if self.cornerPlace:
            return obj, [self.position[0] + offset[0], self.position[1] + offset[1]]
        else:
            return obj, [self.position[0] + offset[0] - width // 2, self.position[1] + offset[1] - height // 2]

    def getRect(self):
        return self.objs[0].get_rect()


#decided to not make this a child class of Structure because of all the wire algorithms, might overwrite some structure functions
class Wire:
    wireAssets = {
        (3, 2) : "3-2-wire.png",
        (2, 3) : "3-2-wire.png",
        (2, 1) : "2-1-wire.png",
        (1, 2): "2-1-wire.png",
        (3, 4) : "3-4-wire.png",
        (4, 3): "3-4-wire.png",
        (3, 1) : "3-1-wire.png",
        (1, 3): "3-1-wire.png",
        (4, 1) : "4-1-wire.png",
        (1, 4): "4-1-wire.png",
        (2, 4) : "2-4-wire.png",
        (4, 2): "2-4-wire.png"
    }
    '''  2
      3  +  1
         4
    '''
    def __init__(self, pixelCornerPosition, initialDirection = 3, finalDirection = 1, leftTile = None, rightTile = None,
                 bottomTile = None, upTile = None):
        self.type = (initialDirection, finalDirection)

        self.wireStructure = Structure(
            f"assets/images/wire/{self.wireAssets[(initialDirection, finalDirection)]}.png",
            -1, "Wire", position=(False, pixelCornerPosition[0], False, pixelCornerPosition[1]), wire = True
        )
        self.prev = None
        self.next = None

        if initialDirection == 1:
            self.prev = rightTile
        elif initialDirection == 2:
            self.prev = upTile
        elif initialDirection == 3:
            self.prev = leftTile
        elif initialDirection == 4:
            self.prev = bottomTile
        else:
            raise Exception()

        if finalDirection == 1:
            self.next = rightTile
        elif finalDirection == 2:
            self.next = upTile
        elif finalDirection == 3:
            self.next = leftTile
        elif finalDirection == 4:
            self.next = bottomTile
        else:
            raise Exception()


