import pygame
import util


class Player(pygame.sprite.Sprite):

    def __init__(self, name, x, y):
        self.image, self.rect = util.load_png('snake.png')
        self.name = name
        self.x = x
        self.y = y
        self.rect = self.rect.move([self.x, self.y])
        self.direction = ''

    def handle_input(self, command):
        self.direction = command

    def update(self):
        if self.direction == 'left':
            self.rect = self.rect.move([-1, 0])
        elif self.direction == 'right':
            self.rect = self.rect.move([1, 0])
        elif self.direction == 'up':
            self.rect = self.rect.move([0, -1])
        elif self.direction == 'down':
            self.rect = self.rect.move([0, 1])


