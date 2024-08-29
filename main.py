from game import *
import json
import os.path

game = Game()

while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            #game.saveGameData()
            pg.quit()
            raise SystemExit

        game.mouse(pg.mouse.get_pos(), pg.mouse.get_pressed())

        if event.type == pg.MOUSEWHEEL:
            game.scroll(event.x, event.y)

        pg.key.set_repeat(1, 90)

        if event.type == pg.KEYDOWN:
            game.record(event.key)

    game.tick()
    pg.display.flip()



