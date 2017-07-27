import pygame
import util
import random

class Food(pygame.sprite.Sprite):
    def __init__(self):
        self.image, self.rect = util.load_png('bunny.png')

    def place_random(self):
        x = random.randint(0, 800)
        y = random.randint(0,600)
        self.rect.center = x,y
        print("Food placed: " + str(x) + " " + str(y))
