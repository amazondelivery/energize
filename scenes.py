import pygame as pg
from screenObject import *
from character import *
from sequence import Sequence
from camera import *
import json
import os.path

class TitleSequence(Sequence):
    def __init__(self):
        super().__init__()
        self.audioToggle = True

        #this whole dictionary thing is only gonna be on the title sequence because I'm just testing it out and seeing how
        #it goes
        self.fonts = {
            "titleFont" : self.font("MajorMonoDisplay-Regular.ttf", 185),
            "buttonFont" : self.font("MajorMonoDisplay-Regular.ttf", 40),
            "textFont" : self.font("AeogoPixellated-DYYEd.ttf", 40)
        }

        self.texts = [
            Text(self.fonts['titleFont'], "ENERGIZE", -1, position=(True, 0, True, 165)),
            Text(self.fonts['buttonFont'], "PLAY", 2, position=(True, 0, True, -30)),
            Text(self.fonts['buttonFont'], "SETTINGS", 1, position=(True, 0, True, -130))
        ]

        self.images = []
        self.characters = []

    def drawHelper(self, screen):
        screen.fill("BLACK")
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



class SettingsSequence(Sequence):
    #need updating to new format
    def __init__(self):
        super().__init__()

        self.fonts = {
            "mainFont" : self.font("AeogoPixellated-DYYEd.ttf", 40)
        }

        self.texts = [
            Text(self.fonts['mainFont'], "Sample Text", -1, position=(True, 0, True, 0))
        ]

        self.images = []
        self.characters = []

    def drawHelper(self, screen):
        screen.fill("PURPLE")
        return screen

    def record(self, char):
        return 0

    def mouse(self, coords, buttonsPressed):
        return -1

class GameScene(Sequence):
    #im not using pickle for game saves
    def __init__(self):
        super().__init__()

        map_width = self.screen_width * 12
        map_height = self.screen_height * 24

        self.camera = Camera()

        self.fonts = {

        }

        self.texts = []

        self.images = [
            Image("map.png", -1, (False, 0, False, 0), (map_width, map_height))
        ]

        self.characters = [
            Player("groo.jpg", -1, (72,69)) #temp player model will be gru from despicable me
        ]

        self.inControl = self.characters[0]

    def drawHelper(self, screen):
        screen.fill("BLACK")
        return screen

    def record(self, char):
        if char == 'w':
            self.inControl.updatePos(0, 15)
        elif char == 'a':
            self.inControl.updatePos(-15, 0)
        elif char == 's':
            self.inControl.updatePos(0, -15)
        elif char == 'd':
            self.inControl.updatePos(15, 0)
        return -1

    def mouse(self, coords, buttonsPressed):
        return -1

    def addSizes(self):
        return 0

    def introScene(self):
        print("intro scene bla bla bla")



