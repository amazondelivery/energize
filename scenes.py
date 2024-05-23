import pygame as pg
from abc import ABC, abstractmethod

class Sequence(ABC):
    @abstractmethod
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
    @abstractmethod
    def record(self, char):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    def mids(self, obj, x = 0, y = 0):
        return (self.screen_width / 2 - obj.get_width() // 2 + x, self.screen_height / 2 - obj.get_height() // 2 - y)

    def mid_height(self, obj):
        return self.mids(self,obj)[0]

    def mid_width(self, obj):
        return self.mids(self,obj)[1]

#java's abstract classes would be perfect here. real shame...
class TitleSequence(Sequence):
    def __init__(self):
        super().__init__()
        self.audioToggle = True
        self.titleFont = pg.font.Font("MajorMonoDisplay-Regular.ttf", 185)
        self.buttonFont = pg.font.Font("MajorMonoDisplay-Regular.ttf", 40) #prob not using this
        self.textFont = pg.font.Font("AeogoPixellated-DYYEd.ttf", 40)

    def draw(self, screen):
        screen.fill("BLACK")
        title = self.titleFont.render("ENERGIZE", True, "White")
        playButton = self.textFont.render("PLAY", True, "White")
        settingsButton = self.textFont.render("SETTINGS", True, "White")

        screen.blit(title, (super().mids(title, 0, 165)))
        screen.blit(playButton, (super().mids(playButton, 0, -30)))
        screen.blit(settingsButton, super().mids(settingsButton, 0, -100))
        return screen

    def record(self, char):
        if char == 'a':
            return 1
        else:
            return -1


class SettingsSequence(Sequence):
    def __init__(self):
        super().__init__()
        self.font = pg.font.Font("AeogoPixellated-DYYEd.ttf", 40)

    def draw(self, screen):
        screen.fill("PURPLE")
        sampleText = self.font.render("hi", True, "BLACK")

        screen.blit(sampleText, (200,200))
        return screen

    def record(self, char):
        return 0

class GameScene(Sequence):
    def __init__(self):
        super().__init__()
        print('game scene initalized')

    def draw(self, screen):
        screen.fill("RED")

        return screen

    def record(self, char):
        return 0
