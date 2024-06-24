from asset import Image

class Structure(Image):
    #probably will not use this class, but im building it just in case
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