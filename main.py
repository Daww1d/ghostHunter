import pygame
import math

import animations
import spriteSheet
import player

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

#hp
tickCooldown = 300
currentDamage = pygame.time.get_ticks()
lastDamage = 0
#stam
stamCooldown = 2000
lastStamTick = pygame.time.get_ticks()
regen = False


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
RED = (255, 0 ,0)
col = RED
GREEN = (0,255, 0)
BLUE = (0,0,255)

bg = pygame.image.load("assets\pixil.png").convert()
bg = pygame.transform.scale(bg, (1200,800))

currentAnimation = {
    "idle" : idleAnimations,
    "walk" : walkAnimations,
    "run" : runAnimations
}

#player
character = player.Player(100,100, "up", 5)

#playerSpeed = 5

def checkInput(key, value):
    if key == pygame.K_a:
        character.inputs["left"] = value
    elif key == pygame.K_d:
        character.inputs["right"] = value
    elif key == pygame.K_w:
        character.inputs["up"] = value
    elif key == pygame.K_s:
        character.inputs["down"] = value
        
def setDirection(key, currentDirection):
    if key == pygame.K_a:
        return "left"
    elif key == pygame.K_d:
        return "right"
    elif key == pygame.K_w:
        return "up"
    elif key == pygame.K_s:
        return "down"

    return currentDirection


#death cube
redCube = pygame.Rect(700, 340, 25, 25)
#wall
wall = pygame.Rect(900,500, 100, 25)
#
topWall = pygame.Rect(0,0, 1200, 65)
bottomWall = pygame.Rect(0,760, 1200, 40)
leftWall = pygame.Rect(0,0, 50, 800)
rightWall = pygame.Rect(1150,0, 50, 800)



while run:

    currentTime =  pygame.time.get_ticks()
    currentDamage = pygame.time.get_ticks()
    currentStamTick = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            checkInput(event.key, True)
            if event.key == pygame.K_LSHIFT:
                character.sprint = True    

            character.direction = setDirection(event.key, character.direction)
        elif event.type == pygame.KEYUP:
            checkInput(event.key, False)
            if event.key == pygame.K_LSHIFT:
                character.sprint = False

#draw map + stuff
    screen.fill(BG)
    playerCollisionBox = pygame.Rect(character.playerX + 1, character.playerY + 1, 62, 62)
    pygame.draw.rect(screen, BLACK, playerCollisionBox)
    screen.blit(bg, (0,0))
    #walls
    pygame.draw.rect(screen, BLACK, topWall)

#stamina + healthbars

    healthBar = pygame.Rect(550,600,character.health * 5,40)
    healthBar.center = (600,695)
    healthBarBorder = pygame.Rect(550,600,character.health * 5 + 10,50)
    healthBarBorder.center = (600,695)

    staminaBar = pygame.Rect(575,675,character.stamina * 5,40)
    staminaBarBorder = pygame.Rect(575,675,character.stamina * 5 + 10,50) 
    staminaBar.center = (600,750)
    staminaBarBorder.center = (600,750)



#coll detection

    col = RED

    wallList = [topWall, bottomWall, leftWall, rightWall]
    collisionList = [redCube]

    #collision detection
    collideState = False


    if collideState == False:
        character.velocity[0] = character.inputs["right"] - character.inputs["left"]
        character.velocity[1] = character.inputs["down"] - character.inputs["up"]
    elif collideState == True:
        character.velocity[0] = 0
        character.velocity[1] = 0
    
    if character.velocity[0] != 0 or character.velocity[1] != 0:
        character.status = "walk"
    if character.sprint == True and (character.velocity[0] != 0 or character.velocity[1] != 0):
        character.status = "run"
    if character.velocity[0] == 0 and character.velocity[1] == 0:
        character.status = "idle"

    if character.sprint == True:
        if character.stamina > 0:
            mult = 1.5
            character.stamina -= 1
        else:
            mult = 1
    else:
        mult = 1
        if character.stamina < character.maxStamina:
            if currentStamTick - lastStamTick >= stamCooldown:
                regen = True
                lastStamTick = currentStamTick

    if character.stamina >= 50:
        regen = False

    if regen == True:
        character.stamina += 1

    #collision checker
    for object in wallList:
        #check for y collisions 
        if object.colliderect(playerCollisionBox.x , playerCollisionBox.y + (character.velocity[1] * character.speed * mult), 62 , 62):
            character.velocity[1] = 0
        #check for x collision
        if object.colliderect(playerCollisionBox.x + (character.velocity[0] * character.speed * mult) , playerCollisionBox.y, 62 , 62):
            character.velocity[0] = 0


    for object in collisionList:
        if object.colliderect(playerCollisionBox):
            col = GREEN
            if currentDamage - lastDamage >= tickCooldown:
                if character.health >= 0:
                    character.health -= 5
                    lastDamage = currentDamage
            #print(f"{object} collision")


    screen.fill(BG)
    playerCollisionBox = pygame.Rect(character.playerX + 1, character.playerY + 1, 62, 62)
    pygame.draw.rect(screen, BLACK, playerCollisionBox)
    screen.blit(bg, (0,0))

    #update animatiion
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

    #DEATH cube
    pygame.draw.rect(screen, col, redCube)

    #draw player

    screen.blit(currentAnimation[character.status][character.direction][frame[character.status]], (character.playerX, character.playerY))

    #draw healthbars

    pygame.draw.rect(screen, BLACK, healthBarBorder)
    pygame.draw.rect(screen, RED, healthBar)
    pygame.draw.rect(screen, BLACK, staminaBarBorder)   
    pygame.draw.rect(screen, BLUE, staminaBar)

    

    #screen.blit(walkR.animation[frame[walkR.type]], (0 , 0) )
    #screen.blit(runR.animation[frame[runR.type]], (70 , 0) )
    #screen.blit(idleL.animation[frame[idleR.type]], (140 , 0) )


    #player movement
    character.playerX += character.velocity[0] * character.speed * mult
    character.playerY += character.velocity[1] * character.speed * mult

    clock.tick(FPS)
    pygame.display.update()


pygame.quit()
