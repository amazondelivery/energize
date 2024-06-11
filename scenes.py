import pygame as pg
from screenObject import *
from sequence import Sequence
from world import World
from player import Player
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

        #initial camera positions
        initialCameraX = 640
        initialCameraY = 360

        #map and player and assets

        #map dimensions
        map_width = self.screen_width * 4
        map_height = self.screen_height * 6

        map = Image("map.png", -1, (False, 0, False, 0), (map_width, map_height))
        player = Player("groo.jpg", -1, (72,69), map_dimensions=(map_width, map_height))
        assets = {
            #"solarBright" : Image("solarBright.png", -1, ),
        }

        self.world = World(map, assets, player, (map_width, map_height), (initialCameraX, initialCameraY))

    #override
    def draw(self, screen):
        screen.fill(self.world.getGradientColor("sunset"))
        self.blit(screen)
        return screen
    #override
    def blit(self, screen):
        self.world.timeIncrease()
        offset = self.world.getCamera().getPlayerOffset(self.world.getPlayer())

        screen.blit(*self.world.getMap().blit(offset))

        for structure in self.world.getStructures():
            screen.blit(*structure.blit(offset))

        screen.blit(*self.world.getPlayer().blit(offset))

    def record(self, char):
        camera = self.world.getCamera()
        if char == 'w':
            self.world.updatePlayer(0, 15)
        elif char == 'a':
            self.world.updatePlayer(-15, 0)
        elif char == 's':
            self.world.updatePlayer(0, -15)
        elif char == 'd':
            self.world.updatePlayer(15, 0)
        elif char == '<':
            camera.moveLeft(15)
        elif char == '>':
            camera.moveRight(15)
        elif char == "^":
            camera.moveUp(15)
        elif char == "|":
            camera.moveDown(15)
        camera.scan(self.world.getPlayer().getPosition())
        return -1

    def mouse(self, coords, buttonsPressed):
        return -1

    def introScene(self):
        print("intro scene bla bla bla")



