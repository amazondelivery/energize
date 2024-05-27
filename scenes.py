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
            "title" : self.fonts["titleFont"].render("ENERGIZE", True, "White"),
            "playButton" : self.fonts["buttonFont"].render("PLAY", True, "White"),
            "settingsButton" : self.fonts["buttonFont"].render("SETTINGS", True, "White")
        }

    def draw(self, screen):
        screen.fill("BLACK")

        screen.blit(self.texts["title"], (super().mids(self.texts["title"], 0, 165)))
        screen.blit(self.texts["playButton"], (super().mids(self.texts["playButton"], 0, -30)))
        screen.blit(self.texts["settingsButton"], super().mids(self.texts["settingsButton"], 0, -130))
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

    def checkCollision(self, buttonRect, mouseClickCoords):
        #rework this to compare to every button isntead of just one button
        if (buttonRect[0] < mouseClickCoords[0] <
            buttonRect[0] + buttonRect[2]) and (buttonRect[1] < mouseClickCoords[1] <
                                                buttonRect[1] + buttonRect[3]):
            return True
        else:
            return False
    def mouse(self, coords, buttonsPressed):

        return -1

class SettingsSequence(Sequence):
    def __init__(self):
        super().__init__()
        self.font = pg.font.Font("AeogoPixellated-DYYEd.ttf", 40)

    def draw(self, screen):
        screen.fill("PURPLE")
        sampleText = self.font.render("hi", True, "BLACK")

        screen.blit(sampleText, (200,200))
        return screen

    def record(self, char):
        return 0

    def mouse(self, coords, buttonsPressed):
        return -1

class GameScene(Sequence):
    #in my attempts to find out how to serialize an object to file in python, literally every guide told me I need to
    #use something called "pickle." Not only is that a silly name, it's amazing that I need to use some unheard of
    #package just to do something so basic. im not using pickle. I will be using json and I don't care if this makes
    #saving data exponentially harder
    def __init__(self):
        super().__init__()
        print('game scene initalized')

    def draw(self, screen):
        screen.fill("RED")

        return screen

    def record(self, char):
        return 0

    def mouse(self, coords, buttonsPressed):
        return -1

    def introScene(self):
        print("intro scene bla bla bla")



