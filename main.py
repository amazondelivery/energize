from game import *
import json
import os.path

game = Game()

#implement all keywords here instead of using if else in the future
keywords = {
    pg.K_a : 'a',
    pg.K_q : 'q',
    pg.K_w : 'w',
    pg.K_s : 's'
}

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
            elif event.key == pg.K_UP:
                game.record('^')
            elif event.key == pg.K_RIGHT:
                game.record('>')
            elif event.key == pg.K_LEFT:
                game.record('<')
            elif event.key == pg.K_DOWN:
                game.record('|')

    game.tick()
    pg.display.flip()



