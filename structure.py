from asset import Image

class Structure(Image):

    def __init__(self, imageName, clickAction,
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

class AnimatedStructure(Structure):
    def __init__(self, imageNames, clickAction, position = (False, 0, False, 0), transformation = None, cornerPlace = True, show = True, startingFrame = 0):
        if transformation == None:
            self.objs = [self.renderImage(imageName, (self.tileDim, self.tileDim)) for imageName in imageNames]
        else:
            self.objs = [self.renderImage(imageName, transformation) for imageName in imageNames]
        self.clickAction = clickAction
        self.position = self.regPosition(position)
        self.cornerPlace = cornerPlace
        self.show = show
        self.frame = startingFrame
        self.animationLength = len(self.objs)
        self.rect = self.getRect()

    def blit(self, offset = (0,0)):
        width, height = self.getWidthHeight()
        positionArray = self.position.copy()

        if self.cornerPlace:
            positionArray[0] = positionArray[0] + offset[0]
            positionArray[1] = positionArray[1] + offset[1]
            return self.objs[self.frame], positionArray
        else:
            positionArray[0] = positionArray[0] + offset[0] - width//2
            positionArray[1] = positionArray[1] + offset[1] - height // 2
            return self.obj[self.frame], positionArray
        self.frame = (self.frame + 1) % self.animationLength


