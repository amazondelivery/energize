import pygame as pg
from scenes import *
import json
import os.path

#i initially was not going to go for an object oriented designed game since the base game is rather small,
# but i took inspiration from this video (https://youtu.be/2gABYM5M0ww?si=sUilwjJvzpKZwtn7) and i decided
# to go with it
class Game:
    def __init__(self):
        #sequences
        self.sceneManager = SceneManager()
        '''
        if self.checkFirstRun():
            self.data = self.prepIntroScene()
        else:
            self.data = self.getGameData()'''

        # why does python make you add "self." every time you use an instance variable. so annoying

    def tick(self):
        self.sceneManager.tick()

    def record(self, char):
        self.sceneManager.record(char)

    def mouse(self, coords, buttonsPressed):
        self.sceneManager.mouse(coords, buttonsPressed)

    def checkFirstRun(self):
        if not os.path.isfile("gameData.json"):
            return True
        else:
            return False

    def saveGameData(self):
        with open('gameData.json', 'w') as gameData:
            json.dump(self.data, gameData)

    def getGameData(self):
        with open("gameData.json") as gameData:
            return json.load(gameData)

    def prepIntroScene(self):
        print("filler")

    #debug purposes
    def screenshot(self):
        self.sceneManager.screenshot()

class SceneManager:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Energize")

        self.screen = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()

        self.sequences = [TitleSequence(), SettingsSequence(), GameScene()]

        #sets intial scene to title screen
        self.currentScene = self.sequences[0]

    def update(self, screen):
        self.screen = self.currentScene.draw(screen)

    def changeScene(self, sequenceNum):
        self.currentScene = self.sequences[sequenceNum]

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
        num = self.currentScene.mouse(coords, buttonsPressed)
        if num != -1:
            self.changeScene(num)

    #debug purposes
    def screenshot(self):
        pg.image.save(self.screen, "screenshot.jpg")




game = Game()

while True:
    for event in pg.event.get():

        if event.type == pg.QUIT:
            '''game.saveGameData()'''
            pg.quit()
            raise SystemExit

        #there is a problem where one single click gets registered as multiple clicks that I will address later
        game.mouse(pg.mouse.get_pos(), pg.mouse.get_pressed())

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:

                game.record('a')

            if event.key == pg.K_q:

                game.record('q')



    game.tick()
    pg.display.flip()



