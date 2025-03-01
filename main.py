import pygame
import math

import animations
import spriteSheet

pygame.init()

# CONSTANTS
WIDTH = 1200
HEIGHT = 800
FPS = 60

run = True

#screen vars
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()

#load assets
sprite_sheet_idle = pygame.image.load("assets\idle.png").convert_alpha()
spriteSheetIdle = spriteSheet.spriteSheet(sprite_sheet_idle)

lastUpdate = pygame.time.get_ticks()
animationCooldown = 250
frame = 0

#animation list
idleR = animations.animation("right", "idle", 4)
for x in range(idleR.loop):
    idleR.animation.append(spriteSheetIdle.get_image(x, 16, 16, 4,))

idleU = animations.animation("up", "idle" , 4)
for x in range(idleU.loop):
    idleU.animation.append(spriteSheetIdle.get_image(x, 16, 16, 4, 2))

idleL = animations.animation("left", "idle" , 4)
for x in range(idleL.loop):
    idleL.animation.append(spriteSheetIdle.get_image(x, 16, 16, 4, 0, 1))

idleD = animations.animation("down", "idle" , 4)
for x in range(idleD.loop):
    idleD.animation.append(spriteSheetIdle.get_image(x, 16, 16, 4, 1))

idleAnimations = {
    "left" : idleL.animation,
    "right" : idleR.animation,
    "down" : idleD.animation,
    "up" : idleU.animation
}


BG = (50, 50, 50)
BLACK = (0, 0, 0)


playerX = 0
playerY = 0
playerInput = {"left": False, "right": False, "up": False, "down": False}
playerVelocity = [0, 0]
playerDirection = "right"

playerSpeed = 5

def checkInput(key, value):
    if key == pygame.K_LEFT:
        playerInput["left"] = value
    elif key == pygame.K_RIGHT:
        playerInput["right"] = value
    elif key == pygame.K_UP:
        playerInput["up"] = value
    elif key == pygame.K_DOWN:
        playerInput["down"] = value

def setDirection(key):
    if key == pygame.K_LEFT:
        playerDirection = "left"
    elif key == pygame.K_RIGHT:
        playerDirection = "right"
    elif key == pygame.K_UP:
        playerDirection = "up"
    elif key == pygame.K_DOWN:
        playerDirection = "down"

    return playerDirection


while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            checkInput(event.key, True)
            playerDirection = setDirection(event.key)
        elif event.type == pygame.KEYUP:
            checkInput(event.key, False)

    playerVelocity[0] = playerInput["right"] - playerInput["left"]
    playerVelocity[1] = playerInput["down"] - playerInput["up"]

    screen.fill(BG)
    #update animatiion
    currentTime =  pygame.time.get_ticks()
    if currentTime - lastUpdate >= animationCooldown:
        frame += 1
        lastUpdate = currentTime
        if frame >= len(idleR.animation):
            frame = 0
        if frame >= len(idleU.animation):
            frame = 0

    screen.blit(idleAnimations[playerDirection][frame], (playerX, playerY))

    screen.blit(idleR.animation[frame], (0 , 0) )
    screen.blit(idleD.animation[frame], (70 , 0) )
    screen.blit(idleL.animation[frame], (140 , 0) )


    playerX += playerVelocity[0] * playerSpeed
    playerY += playerVelocity[1] * playerSpeed

    clock.tick(FPS)
    pygame.display.update()


pygame.quit()
