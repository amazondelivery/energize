import pygame as pg
from screenObject import *
from character import *
from sequence import Sequence
from camera import *
from gradient import *
from world import World
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

        #map dimensions
        map_width = self.screen_width * 4
        map_height = self.screen_height * 6

        world = World((map_width, map_height))

        #initial camera positions
        initialCameraX = 640
        initialCameraY = 360
        self.camera = Camera((map_width, map_height), (initialCameraX, initialCameraY))
        self.gradients = GameGradients()
        self.fonts = {

        }

        self.texts = []

        self.images = [
            Image("map.png", -1, (False, 0, False, 0), (map_width, map_height))
        ]

        self.characters = [
            Player("groo.jpg", -1, (72,69), map_dimensions=(map_width, map_height)) #temp player model will be gru from despicable me
        ]

        #sets the player in control to player 1
        self.inControl = self.characters[0]

        self.timeControl = 0

    def getGradientColor(self, gradientTitle):
        gradient = self.gradients.getGradient(gradientTitle)
        color = gradient.getColor((self.timeControl // (gradient.getTimeStop() * 10)) % gradient.getNumStops())
        return color

    def drawHelper(self, screen):

        #time increment
        self.timeControl += 1

        #gradient fill
        screen.fill(self.getGradientColor("sunset"))

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
        elif char == '<':
            self.camera.moveLeft(15)
        elif char == '>':
            self.camera.moveRight(15)
        elif char == "^":
            self.camera.moveUp(15)
        elif char == "|":
            self.camera.moveDown(15)
        self.camera.scan(self.characters[0].getPosition())
        return -1

    def mouse(self, coords, buttonsPressed):
        return -1

    def blit(self, screen):
        offset = self.camera.getPlayerOffset(self.characters[0])
        for image in self.images:
            screen.blit(*image.blit(offset))
        for text in self.texts:
            screen.blit(*text.blit(offset))
        for character in self.characters:
            screen.blit(*character.blit(offset))

    def introScene(self):
        print("intro scene bla bla bla")



