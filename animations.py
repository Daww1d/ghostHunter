import pygame

import spriteSheet

pygame.init()

class animation():
    def __init__(self, direction, type, loop):
        self.direction = direction
        self.type = type
        self.loop = loop
        self.animation = []

    
