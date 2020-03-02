import pygame
import random
import pygame.locals


# gem is static, no need to update its position
class gemstone(pygame.sprite.Sprite):
    def __init__(self):
        super(gemstone, self).__init__()
        # the image has 20 X 20 pixels
        self.image = pygame.image.load('gemstone.png').convert()
        self.image.set_colorkey((0, 0, 0), pygame.locals.RLEACCEL)
        self.rect = self.image.get_rect(center=(20 * random.randint(0, 19) + 10,
                                                20 * random.randint(0, 29) + 10))
