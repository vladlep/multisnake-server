import pygame
import util
from tail import Tail


SPEED = 3
BLOCK_SIZE = 30

WIDTH = 800 #TODO get from main
HEIGHT = 600 #TODO get from main

class Player(pygame.sprite.Sprite):

    def __init__(self, name, x, y):
        #self.image, self.rect = util.load_png('snake.png')
        #self.rect = pygame.Rect
        super(Player, self).__init__()
        self.color = util.random_color()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.name = name
        self.x = x
        self.y = y
        self.rect = self.rect.move([self.x, self.y])
        self.direction = ''
        self.tail = [ Tail(self, 1) ]
        self.positions = [] #to keep track of where the tail should be drawn

    def get_position_behind(self, nr):
        ''' get the coordinates of *nr* blocks behind me '''
        index = nr * (BLOCK_SIZE / SPEED) + nr + 1 #1 for space in between
        if len(self.positions) < index:
            return (0,0)
        return self.positions[len(self.positions) - index]

    def get_tail_color(self):
        ''' A bit of lighter color for the tail '''
        (r,g,b) = self.color
        return (min(255, r+70), min(255, g+70), min(255, b+70))

    def grow(self):
        self.tail.append(Tail(self, len(self.tail)+1))

    def handle_input(self, command):
        self.direction = command

    def update(self):
        if self.direction == 'left':
            self.rect = self.rect.move([-SPEED, 0])
        elif self.direction == 'right':
            self.rect = self.rect.move([SPEED, 0])
        elif self.direction == 'up':
            self.rect = self.rect.move([0, -SPEED])
        elif self.direction == 'down':
            self.rect = self.rect.move([0, SPEED])
        self.positions.append( (self.rect.x, self.rect.y) ) #TODO this will run out of memory
        if self.rect.x < -BLOCK_SIZE:
            self.rect.x = WIDTH + BLOCK_SIZE
        elif self.rect.x > WIDTH + BLOCK_SIZE:
            self.rect.x = -BLOCK_SIZE
        if self.rect.y < -BLOCK_SIZE:
            self.rect.y = HEIGHT + BLOCK_SIZE
        elif self.rect.y > HEIGHT + BLOCK_SIZE:
            self.rect.y = -BLOCK_SIZE
        for t in self.tail:
            t.update()
