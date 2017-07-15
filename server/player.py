import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def update(self, command):
        if command == 'left':
            self.x -= 1
        elif command == 'right':
            self.x += 1
        elif command == 'up':
            self.y -= 1
        elif command == 'down':
            self.y += 1


