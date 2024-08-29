from screenObject import Text
from sequence import Sequence
from world import World
from asset import GUI, Image
from asset import Text as BetterText
import pygame as pg
import json
import os.path
# main point of this class is to instate world and also translate player inputs to actual changes on screen

keywords = {
    pg.K_a : 'a',
    pg.K_q : 'q',
    pg.K_w : 'w',
    pg.K_s : 's',
    pg.K_d : 'd'
}

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

        self.world = World((self.screen_width, self.screen_height))

        leftAlign = -40
        topAlign = -40
        tileDim = self.world.getTileDim()
        currentlySelectedIconDimension = (tileDim, tileDim)
        self.currentlySelectedIcons = [
            None,
            GUI("assets/images/solarNight.png", currentlySelectedIconDimension, True, left=leftAlign, top=topAlign),
            GUI("assets/images/wire/3-2-wire.png", currentlySelectedIconDimension, True, left=leftAlign, top=topAlign)
        ]

        self.hover = Image("assets/images/Border.png", (False, 0, False, 0), (tileDim, tileDim), True, transparent=True)
        self.guiItems = [
            self.currentlySelectedIcons
        ]

    def draw(self, screen):
        self.worldEvent()
        screen.fill(self.world.getGradientColor("sunrise"))
        self.blit(screen)
        return screen

    def worldEvent(self):
        self.world.timeIncrease()

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

    def record(self, key):
        camera = self.world.getCamera()
        speed = self.world.getPlayer().getSpeed()
        char = keywords.get(key)
        if char == 'w':
            for i in range(speed*2):
                self.world.updatePlayer(0, 1)
        elif char == 'a':
            for i in range(speed*2):
                self.world.updatePlayer(-1, 0)
        elif char == 's':
            for i in range(speed*2):
                self.world.updatePlayer(0, -1)
        elif char == 'd':
            for i in range(speed*2):
                self.world.updatePlayer(1, 0)
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
            self.hover.showWithPosition(self.world.getMap().normalizeTileCornerPosition(mapCursorLocation))
        else:
            self.hover.hideObject()

        leftClick = buttonsPressed[0]
        if leftClick:
            self.click(coords, mapCursorLocation)
            
        return -1

    def click(self, frameCoords, mapCoords):
        if self.world.getMap().outOfMapBounds(mapCoords) or self.world.inPlayersWay(mapCoords):
            print("cant place that here")
            return False
        elif self.world.outOfPlayerRange(mapCoords):
            print("out of range")
            return False
        else:
            self.world.place(mapCoords)
            return True

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





