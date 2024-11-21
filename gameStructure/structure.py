from gameStructure.asset import Image, Text
import pygame as pg
from os import listdir

labelSize = 20
labelUpMove = 20


class Structure(Image):
    def __init__(self, imageName, label,
                 position = (False, 0, False, 0), transformation = None, cornerPlace = True, show = True, wire = False,
                 outputInWatts = 250, transparent = False, clickAction = -1):
        self.outputInWatts = outputInWatts
        self.transparent = transparent
        if transformation is None:
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
        return Text(font, label, pg.Color(255, 255, 255),
                          (False, self.position[0], False, self.position[1] - labelUpMove), show = False)


class VariantStructure(Structure):
    # testing clickAction being a default parameter, and position being a non-default parameter
    def __init__(self, imageFolder, label,
                 position, startingFrame = 0, transformation = None, cornerPlace = True,
                 show = True, wire = False, outputInWatts = 250, transparent = False, clickAction = -1):
        self.outputInWatts = outputInWatts
        self.transparent = transparent
        if transformation is None:
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
        width, height = self.getWidthHeight()
        if self.cornerPlace:
            return obj, [self.position[0] + offset[0], self.position[1] + offset[1]]
        else:
            return obj, [self.position[0] + offset[0] - width // 2, self.position[1] + offset[1] - height // 2]

    def getRect(self):
        return self.objs[0].get_rect()

    def updateFrame(self, number = 1):
        self.frame = (self.frame + number) % self.animationLength


class AnimatedStructure(Structure):
    # this was kind of hard to figure out because at first i tried to make my overloaded blit() function would call
    # the parent Image class blit(), which i found out was very hard to do
    def __init__(self, imageFolder, label, position = (False, 0, False, 0), transformation = None, cornerPlace = True, show = True,
                 startingFrame = 0, wire = False, outputInWatts = 250, transparent = False, clickAction = -1):
        self.outputInWatts = outputInWatts
        self.transparent = transparent
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


class Wire(Structure):

    wireAssets = {
        (3, 2) : "3-2-wire.png",
        (2, 3) : "3-2-wire.png",
        (2, 1) : "2-1-wire.png",
        (1, 2) : "2-1-wire.png",
        (3, 4) : "3-4-wire.png",
        (4, 3) : "3-4-wire.png",
        (3, 1) : "3-1-wire.png",
        (1, 3) : "3-1-wire.png",
        (4, 1) : "4-1-wire.png",
        (1, 4) : "4-1-wire.png",
        (2, 4) : "2-4-wire.png",
        (4, 2) : "2-4-wire.png"
    }
    '''  2
      3  +  1
         4
    '''

    def __init__(self, pixelCornerPosition, initialDirection=3, finalDirection=1, leftTile=None, rightTile=None,
                 bottomTile=None, upTile=None):
        self.outputInWatts = 0
        self.transparent = True
        self.objs = [(imageName, self.renderImage(f"assets/images/wire/{imageName}", (self.tileDim, self.tileDim)))
                     for imageName in listdir(f"assets/images/wire")]
        self.clickAction = -1
        self.position = tuple(pixelCornerPosition)
        self.cornerPlace = True
        self.frame = self.startingFrameCalculator()
        self.objsLength = len(self.objs)
        self.rect = self.getRect()
        self.isWire = True
        self.label = self.initLabel("Wire")
        self.show = True

        self.type = (initialDirection, finalDirection)
        self.prev = None
        self.next = None
        self.scrollLength = 4

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

    def startingFrameCalculator(self):
        return 0

    def update(self):
        self.scrollLength += 1

    def blit(self, offset=(0, 0)):
        imageName = self.wireAssets[self.type]
        for images in self.objs:
            if images[0] == imageName:
                obj = images[1]

        for i in range(len(self.objs)):
            if self.objs[i % self.objsLength][0] == imageName:
                obj = self.objs[(i + self.scrollLength) % self.objsLength][1]
        width, height = self.getWidthHeight()
        if self.cornerPlace:
            return obj, [self.position[0] + offset[0], self.position[1] + offset[1]]
        else:
            return obj, [self.position[0] + offset[0] - width // 2, self.position[1] + offset[1] - height // 2]

    def getRect(self):
        return self.objs[0][1].get_rect()


class Transformer(AnimatedStructure):

    def __init__(self, imageFolder, label, position = (False, 0, False, 0), transformation = None, cornerPlace = True, show = True,
                 startingFrame = 0, wire = False, transparent = False, clickAction = -1):
        super().__init__(self, imageFolder, label, position, transformation, cornerPlace, show,
                 startingFrame, wire, transparent, clickAction)

        self.collection = 0

    def updateCollection(self, num):
        self.collection += num








