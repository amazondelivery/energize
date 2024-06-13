import pygame as pg
from screenObject import *
from sequence import Sequence
from world import World
from player import Player
import json
import os.path

#main point of this class is to instate world and also translate player inputs to actual changes on screen

class TitleSequence(Sequence):
    def __init__(self):
        super().__init__()
        self.audioToggle = True

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

    def draw(self, screen):
        screen.fill(self.world.getGradientColor("sunset"))
        self.worldEvent()
        self.blit(screen)
        return screen

    def worldEvent(self):
        self.world.timeIncrease()
        tile = self.world.getPlayerTile()  #unused so far

    def blit(self, screen):
        offset = self.world.getCamera().getPlayerOffset(self.world.getPlayer())

        screen.blit(*self.world.getMap().blit(offset))

        for structure in self.world.getStructures():
            screen.blit(*structure.blit(offset))

        screen.blit(*self.world.getPlayer().blit(offset))

    def record(self, char):
        camera = self.world.getCamera()
        speed = self.world.getPlayer().getSpeed()
        if char == 'w':
            self.world.updatePlayer(0, speed)
            self.world.updatePlayer(0, speed)
        elif char == 'a':
            self.world.updatePlayer(-speed, 0)
            self.world.updatePlayer(-speed, 0)
        elif char == 's':
            self.world.updatePlayer(0, -speed)
            self.world.updatePlayer(0, -speed)
        elif char == 'd':
            self.world.updatePlayer(speed, 0)
            self.world.updatePlayer(speed, 0)
        elif char == '<':
            camera.moveLeft(speed)
        elif char == '>':
            camera.moveRight(speed)
        elif char == "^":
            camera.moveUp(speed)
        elif char == "|":
            camera.moveDown(speed)
        camera.scan(self.world.getPlayer().getPosition())
        return -1

    def mouse(self, coords, buttonsPressed):
        if buttonsPressed[0] == True:
            self.world.leftClick(*coords)
        return -1


