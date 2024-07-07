from asset import Image, Text
import pygame as pg
from os import listdir

labelSize = 20
labelUpMove = 20
class Structure(Image):
    def __init__(self, imageName, clickAction, label,
                 position = (False, 0, False, 0), transformation = None, cornerPlace = True, show = True):
        if transformation == None:
            self.obj = self.renderImage(imageName, (self.tileDim, self.tileDim))
        else:
            self.obj = self.renderImage(imageName, transformation)
        self.clickAction = clickAction
        self.position = self.regPosition(position)
        self.cornerPlace = cornerPlace
        self.show = show
        self.rect = self.getRect()

        self.label = self.initLabel(label)

    def blitLabel(self, offset):
        return self.label.blit(offset)

    def getBlitShow(self):
        return self.label.getShow()

    def showCaption(self):
        self.label.showObject()

    def hideCaption(self):
        self.label.hideObject()

    def initLabel(self, label):
        font = pg.font.Font("assets/fonts/MajorMonoDisplay-Regular.ttf", labelSize)
        return Text(font, label, -1, pg.Color(255, 255, 255),
                          (False, self.position[0], False, self.position[1] - labelUpMove), show = False)

class AnimatedStructure(Structure):
    #this was kind of hard to figure out because at first i tried to make my overloaded blit() function would call
    #the parent Image class blit(), which i found out was very hard to do
    def __init__(self, imageFolder, clickAction, label, position = (False, 0, False, 0), transformation = None, cornerPlace = True, show = True, startingFrame = 0):
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


