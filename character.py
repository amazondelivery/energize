class Character():
    def __init__(self):
        self.speed = 2
        self.direction = [0,0]

class Player(Character):
    def __init__(self):
        super().__init__()
