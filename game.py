from sceneManager import *
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

    def scroll(self, x, y):
        self.sceneManager.scroll(x, y)

    #debug purposes
    def screenshot(self):
        self.sceneManager.screenshot()
