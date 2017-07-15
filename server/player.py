import pygame
import util


class Player(pygame.sprite.Sprite):

    def __init__(self, name, x, y):
        self.image, self.rect = util.load_png('snake.png')
        self.name = name
        self.x = x
        self.y = y
        self.update('')

    def update(self, command):
        if command == 'left':
            self.x -= 1
        elif command == 'right':
            self.x += 1
        elif command == 'up':
            self.y -= 1
        elif command == 'down':
            self.y += 1

        self.rect = self.rect.move([self.x, self.y])


