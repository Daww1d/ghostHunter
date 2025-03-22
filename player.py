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
        self.health = 100
        self.maxHealth = 100
        self.stamina = 50
        self.maxStamina = 50
        self.collided = False