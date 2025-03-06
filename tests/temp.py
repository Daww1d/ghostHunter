import pygame

pygame.init()

# CONSTANTS

WIDTH = 1200
HEIGHT = 800
FPS = 60


# CLASSES
class Button:
    def __init__(self, txt, pos):
        self.text = txt
        # self.size = size #tuple
        self.pos = pos
        self.button = pygame.rect.Rect(
            (self.pos[0], self.pos[1]), (210, 50)
        )  # x and y coordinates

    def draw(self, offsetX=15, offsetY=10):
        btn = pygame.draw.rect(screen, "grey", self.button, 0, 5)
        pygame.draw.rect(screen, "dark grey", self.button, 5, 5)
        text = font.render("Menu", True, "white")
        screen.blit(text, (self.pos[0] + offsetX, self.pos[1] + offsetY))

    def checkClick(self):
        if (
            self.button.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
        ):
            return True
        else:
            return False


class UI:
    def __init__(self):
        self.mainMenu = False

    # Draws main Menu
    def drawMenu(self):
        menuBtn = pygame.draw.rect(screen, "grey", [495, 100, 210, 50], 0, 5)
        pygame.draw.rect(screen, "dark grey", [495, 100, 210, 50], 5, 5)
        text = font.render("Play", True, "white")
        screen.blit(text, (510, 110))
        if (
            menuBtn.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
        ):
            UI.mainMenu = False
        else:
            UI.mainMenu = True
        return UI.mainMenu

    # Drawss main game
    def drawMain(self):
        # menuBtn = pygame.draw.rect(screen, "grey", [495, 10, 210, 50], 0, 5)
        # screen.blit(text, (510, 20))
        button = Button("Menu", (510, 20))
        button.draw()
        return button.checkClick()


screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Menu")
timer = pygame.time.Clock()
font = pygame.font.Font("assets\mainFont.TTF", 24)


run = True

UI = UI()
# GAME LOOP

while run:
    screen.fill("light blue")
    timer.tick(FPS)
    if UI.mainMenu:
        UI.mainMenu = UI.drawMenu()
    else:
        UI.mainMenu = UI.drawMain()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
