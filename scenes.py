import pygame as pg

#java's abstract classes would be perfect here. real shame...
class TitleSequence:
    def __init__(self):
        self.audioToggle = True
        self.titleFont = pg.font.Font("MajorMonoDisplay-Regular.ttf", 150)

    def draw(self, screen):
        text = self.titleFont.render("ENERGIZE", True, "White")
        screen.blit(text, (200,200))
        return screen

    def record(self, char):
        if char == 'a':
            print("a pressed")
            return 1
        else:
            return -1


class SettingsSequence:
    def __init__(self):
        print("settings seq initialized")

    def draw(self, screen):
        screen.fill("PURPLE")
        return screen

class GameScene:
    def __init__(self):
        print('game scene initalized')
