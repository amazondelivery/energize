import pygame as pg
from sceneManager import *
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



