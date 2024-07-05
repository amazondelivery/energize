from asset import Image, Text
import pygame as pg
from os import listdir

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

        self.font = pg.font.Font("assets/fonts/MajorMonoDisplay-Regular.ttf", 25)
        self.label = Text(self.font, label, -1, pg.Color(255, 255, 255),
                          (False, self.position[0], False, self.position[1]), show = False)

    def blitLabel(self, offset):
        return self.label.blit(offset)

    def getBlitShow(self):
        return self.label.getShow()

class AnimatedStructure(Structure):
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


        self.font = pg.font.Font("assets/fonts/MajorMonoDisplay-Regular.ttf", 25)
        self.label = Text(self.font, label, -1, pg.Color(255, 255, 255),
                          (False, self.position[0], False, self.position[1]), show = False)

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

    def blitLabel(self, offset):
        return self.label.blit(offset)

    def getBlitShow(self):
        return self.label.getShow()

