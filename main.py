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

sprite_sheet_run = pygame.image.load("assets\sprint.png").convert_alpha()
spriteSheetRun = spriteSheet.spriteSheet(sprite_sheet_run)

#clcok and animation timer
lastUpdate = pygame.time.get_ticks()
animationCooldown = 250
idleFrame = 0
runFrame = 0
walkFrame = 0
 
#animation list

#idle
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

#walking
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

#running
runR = animations.animation("right", "run", 8)
for x in range(runR.loop):
    runR.animation.append(spriteSheetRun.get_image(x, 16, 16, 4,))

runU = animations.animation("up", "run" , 8)
for x in range(runU.loop):
    runU.animation.append(spriteSheetRun.get_image(x, 16, 16, 4, 2))

runL = animations.animation("left", "run" , 8)
for x in range(runL.loop):
    runL.animation.append(spriteSheetRun.get_image(x, 16, 16, 4, 0, 1))

runD = animations.animation("down", "run" , 8)
for x in range(runD.loop):
    runD.animation.append(spriteSheetRun.get_image(x, 16, 16, 4, 1))

runAnimations = {
    "left" : runL.animation,
    "right" : runR.animation,
    "down" : runD.animation,
    "up" : runU.animation
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
sprintStatus = False
currentAnimation = {
    "idle" : idleAnimations,
    "walk" : walkAnimations,
    "run" : runAnimations
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
            if event.key == pygame.K_LSHIFT:
                sprintStatus = True    

            playerDirection = setDirection(event.key, playerDirection)
        elif event.type == pygame.KEYUP:
            checkInput(event.key, False)
            if event.key == pygame.K_LSHIFT:
                sprintStatus = False

    playerVelocity[0] = playerInput["right"] - playerInput["left"]
    playerVelocity[1] = playerInput["down"] - playerInput["up"]
    
    if playerVelocity[0] != 0 or playerVelocity[1] != 0:
        playerStatus = "walk"
    if sprintStatus == True and (playerVelocity[0] != 0 or playerVelocity[1] != 0):
        playerStatus = "run"
    if playerVelocity[0] == 0 and playerVelocity[1] == 0:
        playerStatus = "idle"

    screen.fill(BG)
    screen.blit(bg, (0,0))
    
    #update animatiion
    currentTime =  pygame.time.get_ticks()
    if currentTime - lastUpdate >= animationCooldown:
        idleFrame += 1
        walkFrame += 1
        runFrame += 1
        lastUpdate = currentTime
        #if frame >= len(currentAnimation[playerStatus][playerDirection]): #bug here not sure how to fix
        if idleFrame >= len(idleD.animation):
            idleFrame = 0
        if walkFrame >= len(walkD.animation):
            walkFrame = 0
        if runFrame >= len(runD.animation):
            runFrame = 0


    frame = {
    "idle" : idleFrame,
    "walk" : walkFrame,
    "run" : runFrame
    }

    #player
    screen.blit(currentAnimation[playerStatus][playerDirection][frame[playerStatus]], (playerX, playerY))

    screen.blit(walkR.animation[frame[walkR.type]], (0 , 0) )
    screen.blit(runR.animation[frame[runR.type]], (70 , 0) )
    screen.blit(idleL.animation[frame[idleR.type]], (140 , 0) )


    if sprintStatus == True:
        mult = 1.5
    else:
        mult = 1

    playerX += playerVelocity[0] * playerSpeed * mult
    playerY += playerVelocity[1] * playerSpeed * mult

    clock.tick(FPS)
    pygame.display.update()


pygame.quit()
