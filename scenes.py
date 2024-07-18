import pygame as pg
from screenObject import Text
from sequence import Sequence
from character import Player
from world import World
from asset import GUI, Image
from asset import Text as BetterText
import json
import os.path
# main point of this class is to instate world and also translate player inputs to actual changes on screen


class TitleSequence(Sequence):
    def __init__(self):
        super().__init__()
        self.audioToggle = True

        self.fonts = {
            "titleFont" : self.font("assets/fonts/MajorMonoDisplay-Regular.ttf", 185),
            "buttonFont" : self.font("assets/fonts/MajorMonoDisplay-Regular.ttf", 40),
            "textFont" : self.font("assets/fonts/AeogoPixellated-DYYEd.ttf", 40)
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
            "mainFont" : self.font("assets/fonts/AeogoPixellated-DYYEd.ttf", 40)
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
    # im not using pickle for game saves
    def __init__(self):
        super().__init__()

        #initial camera positions
        initialCameraX = 640
        initialCameraY = 360

        #map and p

        currentSelectionImage = None
        # add currentSelectionImage to guiItems below

        self.world = World((self.screen_width, self.screen_height))
        tileDim = self.world.getTileDim()
        self.currentlySelectedIcons = [
            None,
            GUI("assets/images/solarNight.png", -1, (80, 80), True, left=-40, top=-40),
            GUI("assets/images/wire/3-2-wire.png", -1, (80, 80), True, left=-40, top=-40)
        ]
        self.hover = Image("assets/images/Border.png", -1, (False, 0, False, 0), (tileDim + 5, tileDim + 5), True, transparent=True)
        self.guiItems = [
            self.currentlySelectedIcons
        ]

    def draw(self, screen):
        screen.fill(self.world.getGradientColor("sunset"))
        self.worldEvent()
        self.blit(screen)
        # print(self.world.getSelectedItem())
        return screen

    def worldEvent(self):
        self.world.timeIncrease()
        tile = self.world.getPlayerTile()  #unused so far

    def blitMap(self, screen, offset):
        screen.blit(*self.world.getMap().blit(offset))

    def blitStructures(self, screen, structureList, offset):
        blitStructureCaption = None
        for structure in structureList:
            if structure.getShow() == True:
                screen.blit(*structure.blit(offset))
                if structure.getBlitShow() == True:
                    blitStructureCaption = structure
        return blitStructureCaption

    def blitPlayer(self, screen, offset):
        screen.blit(*self.world.getPlayer().blit(offset))

    def blitStructureHoverCaption(self, screen, offset, blitStructureCaption):
        if blitStructureCaption != None:
            screen.blit(*blitStructureCaption.blitLabel(offset))

    def blitCurrentlySelectedIcon(self, screen, offset):
        currentlySelected = self.currentlySelectedIcons[self.world.getCurrentSelection()]
        if currentlySelected != None and currentlySelected.getShow() == True:
            screen.blit(*currentlySelected.blit())

    def blitHoverTile(self, screen, offset):
        if self.hover.getShow() == True:
            screen.blit(*self.hover.blit(offset))

    def blit(self, screen):
        offset = self.world.getCameraOffset()

        self.blitMap(screen, offset)

        blitStructureCaption = self.blitStructures(screen, self.world.getStructures(), offset)

        self.blitPlayer(screen, offset)

        self.blitStructureHoverCaption(screen, offset, blitStructureCaption)

        self.blitCurrentlySelectedIcon(screen, offset)

        self.blitHoverTile(screen, offset)

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
        return -1

    def mouse(self, coords, buttonsPressed):
        mapCursorLocation = self.world.getMap().getUniversalCornerPosition()
        mapCursorLocation[0] += coords[0]
        mapCursorLocation[1] += coords[1]

        if self.world.hover(coords, mapCursorLocation):
            self.hover.showWithPosition(self.world.normalizeTileCornerPosition(mapCursorLocation))
        else:
            self.hover.hideObject()

        leftClick = buttonsPressed[0]
        if leftClick:
            self.world.click(coords, mapCursorLocation)
            
        return -1

    def scroll(self, x, y):
        self.world.updateSelectedItem(y)


class LoadingScreenInitial(Sequence):
    def __init__(self):
        super().__init__()

        loadingFont = self.font("assets/fonts/MajorMonoDisplay-Regular.ttf", 80)

        self.texts = [
            BetterText(loadingFont, "Loading", -1, position=(True, 0, True, 0))
        ]

    def drawHelper(self, screen):
        screen.fill("PURPLE")
        return screen

    def record(self, char):
        return 0

    def mouse(self, coords, buttonsPressed):
        return -1

    def blit(self, screen):
        for image in self.images:
            screen.blit(*image.blit()) #test value
        for text in self.texts:
            screen.blit(*text.blit())
        for character in self.characters:
            screen.blit(*character.blit())

    def initializeGame(self):
        return [TitleSequence(), SettingsSequence(), GameScene()]





