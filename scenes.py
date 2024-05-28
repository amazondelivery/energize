import pygame as pg
import json
import os.path
from abc import ABC, abstractmethod

class Sequence(ABC):
    @abstractmethod
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.fonts = {}
        self.texts = {}

    @abstractmethod
    def record(self, char):
        pass

    @abstractmethod
    def mouse(self, coords, buttonsPressed):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def addSizes(self):
        pass

    def blit(self, screen):
        for text in self.texts.values():
            screen.blit(text[0], text[1])

    def checkCollision(self, mouseClickCoords):
        for text in self.texts.keys():

            textCoords = self.texts[text][0].get_rect()
            xMouse = mouseClickCoords[0]
            yMouse = mouseClickCoords[1]
            xInit = self.texts[text][1][0]
            yInit = self.texts[text][1][1]
            xText = textCoords[0]
            yText = textCoords[1]
            textLength = textCoords[2]
            textHeight = textCoords[3]

            if ((xText + xInit <= xMouse <= xText + xInit + textLength)
                    and (yText + yInit <= yMouse <= yText + yInit + textHeight)):
                return text

        return None

    def mids(self, obj, x = 0, y = 0):
        return (self.screen_width / 2 - obj.get_width() // 2 + x, self.screen_height / 2 - obj.get_height() // 2 - y)

    def mid_height(self, obj):
        return self.mids(self,obj)[0]

    def mid_width(self, obj):
        return self.mids(self,obj)[1]

#java's abstract classes would be perfect here. real shame...
class TitleSequence(Sequence):
    def __init__(self):
        super().__init__()
        self.audioToggle = True

        #this whole dictionary thing is only gonna be on the title sequence because I'm just testing it out and seeing how
        #it goes
        self.fonts = {
            "titleFont" : pg.font.Font("MajorMonoDisplay-Regular.ttf", 185),
            "buttonFont" :   pg.font.Font("MajorMonoDisplay-Regular.ttf", 40), #prob not using this
            "textFont" : pg.font.Font("AeogoPixellated-DYYEd.ttf", 40)
        }

        self.texts = {
            "title" : [self.fonts["titleFont"].render("ENERGIZE", True, "White")],
            "playButton" : [self.fonts["buttonFont"].render("PLAY", True, "White")],
            "settingsButton" : [self.fonts["buttonFont"].render("SETTINGS", True, "White")]
        }
        self.addSizes()

    def draw(self, screen):
        screen.fill("BLACK")
        self.blit(screen)
        return screen

    def record(self, char):
        if char == 'a':
            #changes scene to settings page
            return 1
        elif char == 'q':
            #changes scene to game
            return 2
        else:
            return -1

    def addSizes(self):

        #set positions for buttons here
        title = (self.mids(self.texts["title"][0], 0, 165))
        playButton = (self.mids(self.texts["playButton"][0], 0, -30))
        settingsButton = (self.mids(self.texts["settingsButton"][0], 0, -130))

        self.texts["title"].append(title)
        self.texts["playButton"].append(playButton)
        self.texts["settingsButton"].append(settingsButton)

    #currently debugging
    def mouse(self, coords, buttonsPressed):
        collisionButton = self.checkCollision(coords)
        if buttonsPressed[0] == True:
            if collisionButton == "playButton":
                return 2
            elif collisionButton == "settingsButton":
                return 1
        return -1

class SettingsSequence(Sequence):
    def __init__(self):
        super().__init__()

        self.fonts = {
            "mainFont" : pg.font.Font("AeogoPixellated-DYYEd.ttf", 40)
        }
        self.texts = {
            "sampleText" : [self.fonts["mainFont"].render("hi", True, "BLACK")]
        }
        self.addSizes()

    def draw(self, screen):
        screen.fill("PURPLE")
        self.blit(screen)
        return screen

    def record(self, char):
        return 0

    def addSizes(self):
        sampleText = (200,200)

        self.texts["sampleText"].append(sampleText)
    def mouse(self, coords, buttonsPressed):
        return -1

class GameScene(Sequence):
    #in my attempts to find out how to serialize an object to file in python, literally every guide told me I need to
    #use something called "pickle." Not only is that a silly name, it's amazing that I need to use some unheard of
    #package just to do something so basic. im not using pickle. I will be using json and I don't care if this makes
    #saving data exponentially harder
    def __init__(self):
        super().__init__()

        self.fonts = {

        }

        self.texts = {

        }

        self.addSizes()

    def draw(self, screen):
        screen.fill("RED")

        return screen

    def record(self, char):
        return 0

    def mouse(self, coords, buttonsPressed):
        return -1

    def addSizes(self):
        return 0

    def introScene(self):
        print("intro scene bla bla bla")



