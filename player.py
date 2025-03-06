class Player:

    def __init__(self , x, y, initDirection, speed):
        self.playerX = x
        self.playerY = y
        self.inputs = {"left": False,
                       "right": False,
                       "up": False,
                       "down": False}
        self.velocity = [0,0]
        self.direction = initDirection
        self.status = "idle"
        self.sprint = False
        self.speed = speed