import pygame as pg
from scenes import *


class SceneManager:

    mouseIgnoreCapacity = 2

    def __init__(self):
        pg.init()
        pg.display.set_caption("Energize")

        self.screen = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()

        self.sequences = [TitleSequence(), SettingsSequence(), GameScene()]

        #sets intial scene to title screen
        self.currentScene = self.sequences[0]

        self.mouseIgnoreFrames = 0

    def update(self, screen):
        self.screen = self.currentScene.draw(screen)

    def changeScene(self, sequenceNum):
        self.currentScene = self.sequences[sequenceNum]

    def drawHelper(self, screen):
        return screen

    def getSceneName(self):
        return self.currentScene.getName()

    def tick(self):
        self.clock.tick(60)
        self.update(self.screen)

    def record(self, char):
        num = self.currentScene.record(char)
        if num != -1:
            self.changeScene(num)

    def mouse(self, coords, buttonsPressed):
        if buttonsPressed[0] == True:
            if self.mouseIgnoreFrames > 0:
                self.currentScene.mouse(coords, (False, False, False))
                return
            else:
                self.mouseIgnoreFrames = self.mouseIgnoreCapacity
        self.mouseIgnoreFrames -= 1
        num = self.currentScene.mouse(coords, buttonsPressed)
        if num != -1:
            self.changeScene(num)

    #debug purposes
    def screenshot(self):
        pg.image.save(self.screen, "screenshot.jpg")


