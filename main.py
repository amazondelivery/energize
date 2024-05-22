import pygame as pg

pg.init()
titleFont = pg.font.Font("MajorMonoDisplay-Regular.ttf", 150)

screen_width = 1280
screen_height = 720
screen = pg.display.set_mode((screen_width, screen_height))

clock = pg.time.Clock()

#i initially was not going to go for an object oriented designed game, but i took inspiration from
# this video (https://youtu.be/2gABYM5M0ww?si=sUilwjJvzpKZwtn7)
class Game:
    def __init__(self):
        print('hi')

def title():
    text = titleFont.render("ENERGIZE", True, "White")
    screen.blit(text, (200,200))

while True:
    title()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    clock.tick(60)
    pg.display.flip()
