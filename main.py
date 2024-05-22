import pygame as pg
from scenes import *

#i initially was not going to go for an object oriented designed game since the base game is rather small,
# but i took inspiration from this video (https://youtu.be/2gABYM5M0ww?si=sUilwjJvzpKZwtn7) and i decided
# to go with it
class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Energize")

        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pg.time.Clock()

        #sequences
        self.sceneManager = SceneManager()

    def tick(self):
        self.clock.tick(60)

    def mids(self, obj):
        return (self.screen_height / 2 - obj.get_height() // 2, self.screen_width / 2 - obj.get_width() // 2)

    def mid_height(self, obj):
        return self.mids(self,obj)[0]

    def mid_width(self, obj):
        return self.mids(self,obj)[1]

class SceneManager:
    def __init__(self):
        sequences = [TitleSequence()]

        #sets intial scene to title screen
        self.currentScene = sequences[0]

    def drawScene(self):
        self.currentScene.draw()

    def getScene(self):
        return self.currentScene.getName()



game = Game()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

    game.tick()
    pg.display.flip()
