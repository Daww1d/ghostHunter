import pygame

BLACK = (0, 0, 0)


class spriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, row=0, x=False, y=False):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((80 * frame), (row * 80), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image = pygame.transform.flip(image, x, y)
        image.set_colorkey(BLACK)

        return image
