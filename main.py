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

sprite_sheet_walk = pygame.image.load("assets\walk.png").convert_alpha()
spriteSheetWalk = spriteSheet.spriteSheet(sprite_sheet_walk)

#clcok and animation timer
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

walkR = animations.animation("right", "walk", 8)
for x in range(walkR.loop):
    walkR.animation.append(spriteSheetWalk.get_image(x, 16, 16, 4,))

walkU = animations.animation("up", "walk" , 8)
for x in range(walkU.loop):
    walkU.animation.append(spriteSheetWalk.get_image(x, 16, 16, 4, 2))

walkL = animations.animation("left", "walk" , 8)
for x in range(walkL.loop):
    walkL.animation.append(spriteSheetWalk.get_image(x, 16, 16, 4, 0, 1))

walkD = animations.animation("down", "walk" , 8)
for x in range(walkD.loop):
    walkD.animation.append(spriteSheetWalk.get_image(x, 16, 16, 4, 1))

walkAnimations = {
    "left" : walkL.animation,
    "right" : walkR.animation,
    "down" : walkD.animation,
    "up" : walkU.animation
}


BG = (50, 50, 50)
BLACK = (0, 0, 0)


bg = pygame.image.load("assets\grass.png").convert()
bg = pygame.transform.scale(bg, (1200,800))

playerX = 100
playerY = 100
playerInput = {"left": False, "right": False, "up": False, "down": False}
playerVelocity = [0, 0]
playerDirection = "right"
playerStatus = "idle"
currentAnimation = {
    "idle" : idleAnimations,
    "walk" : walkAnimations
}

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

def setDirection(key ,currentDirection):
    if key == pygame.K_LEFT:
        return "left"
    elif key == pygame.K_RIGHT:
        return "right"
    elif key == pygame.K_UP:
        return "up"
    elif key == pygame.K_DOWN:
        return "down"

    return currentDirection


while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            checkInput(event.key, True)
            playerDirection = setDirection(event.key, playerDirection)
        elif event.type == pygame.KEYUP:
            checkInput(event.key, False)

    playerVelocity[0] = playerInput["right"] - playerInput["left"]
    playerVelocity[1] = playerInput["down"] - playerInput["up"]
    
    if playerVelocity[0] != 0 or playerVelocity[1] != 0:
        playerStatus = "walk"
    else:
        playerStatus = "idle"

    screen.fill(BG)
    screen.blit(bg, (0,0))
    
    #update animatiion
    currentTime =  pygame.time.get_ticks()
    if currentTime - lastUpdate >= animationCooldown:
        frame += 1
        lastUpdate = currentTime
        #if frame >= len(currentAnimation[playerStatus][playerDirection]): #bug here not sure how to fix
        if frame >= 4: 
            frame = 0

    screen.blit(currentAnimation[playerStatus][playerDirection][frame], (playerX, playerY))

    screen.blit(idleR.animation[frame], (0 , 0) )
    screen.blit(idleD.animation[frame], (70 , 0) )
    screen.blit(idleL.animation[frame], (140 , 0) )


    playerX += playerVelocity[0] * playerSpeed
    playerY += playerVelocity[1] * playerSpeed

    clock.tick(FPS)
    pygame.display.update()


pygame.quit()
