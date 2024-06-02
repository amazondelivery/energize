import pygame as pg
from game import *
import json
import os.path

#i initially was not going to go for an object oriented designed game since the base game is rather small,
# but i took inspiration from this video (https://youtu.be/2gABYM5M0ww?si=sUilwjJvzpKZwtn7) and i decided
# to go with it

game = Game()

while True:
    for event in pg.event.get():

        if event.type == pg.QUIT:
            '''game.saveGameData()'''
            pg.quit()
            raise SystemExit

        #there is a problem where one single click gets registered as multiple clicks that I will address later
        game.mouse(pg.mouse.get_pos(), pg.mouse.get_pressed())

        pg.key.set_repeat(1, 90)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                game.record('a')
            elif event.key == pg.K_q:
                game.record('q')
            elif event.key == pg.K_w:
                game.record('w')
            elif event.key == pg.K_s:
                game.record('s')
            elif event.key == pg.K_d:
                game.record('d')

    game.tick()
    pg.display.flip()



