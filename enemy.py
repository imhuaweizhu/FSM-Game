import pygame
import pygame.locals
import random
import numpy as np


class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(enemy, self).__init__()
        # the image has 20 X 20 pixels
        self.image = pygame.image.load('enemy.png').convert()
        # RLEACCEL is a optional parameter that will help PyGame render faster on non-accelerated displays.
        self.image.set_colorkey((255, 255, 255), pygame.locals.RLEACCEL)
        self.rect = self.image.get_rect(center=(20 * random.randint(0, 19) + 10,
                                                20 * random.randint(0, 29) + 10))
        self.speed = 20  # 20 pixels is one cell on the screen
        self.goUp = np.array([0, 1])
        self.goDown = np.array([0, -1])
        self.goRight = np.array([1, 0])
        self.goLeft = np.array([-1, 0])

    def update(self):
        '''requirement: Enemies randomly move up, down, left, and right at each time step.'''
        randomDirection = random.choice([self.goUp,
                                         self.goDown,
                                         self.goRight,
                                         self.goLeft])
        stepX = self.speed * randomDirection[0]
        stepY = self.speed * randomDirection[1]
        self.rect.move_ip(stepX, stepY)

        # Keep the enemy on the screen
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= 400:
            self.rect.right = 400
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
