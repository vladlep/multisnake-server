import pygame
import util
import random

import config

class Food(pygame.sprite.Sprite):
    def __init__(self):
        self.image, self.rect = util.load_png('bunny.png')

    def place_random(self):
        x = random.randint(0, config.SCREEN_WIDTH)
        y = random.randint(0, config.SCREEN_HEIGHT)
        self.rect.center = x,y
        print("Food placed: " + str(x) + " " + str(y))
