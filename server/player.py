import pygame
import util
import config
import random

from tail import Tail


SPEED = 5
BLOCK_SIZE = 30
HALF_BLOCK = 0.5 * BLOCK_SIZE

START_POS_X = [0, config.SCREEN_WIDTH-BLOCK_SIZE]
START_POS_Y = [0, config.SCREEN_HEIGHT-BLOCK_SIZE]

class Player(pygame.sprite.Sprite):

    def __init__(self, name):
        #self.image, self.rect = util.load_png('snake.png')
        #self.rect = pygame.Rect
        super(Player, self).__init__()
        self.color = util.random_color()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.name = name
        self.score = 0
        self.pause = 0
        self.group = pygame.sprite.Group()
        self.collidable_tail_group = pygame.sprite.Group() #Everything except the first tail (because you will hit it always on turns)
        self.reset()

    def reset(self):
        self.rect.x = START_POS_X[random.randint(0,1)]
        self.rect.y = START_POS_Y[random.randint(0,1)]
        self.dead = False
        self.direction = ''
        self.positions = [] #to keep track of where the tail should be drawn

        tail = Tail(self, 1)
        self.tail = [ tail ]

        self.group.empty()
        self.group.add(self)
        self.group.add(tail)

        self.collidable_tail_group.empty()

    def get_group(self):
        return self.group

    def get_position_behind(self, nr):
        ''' get the coordinates of *nr* blocks behind me '''
        index = nr * (BLOCK_SIZE / SPEED) + nr + 1 #1 for space in between
        if len(self.positions) < index:
            return (self.rect.x,self.rect.y)
        return self.positions[len(self.positions) - index]

    def get_tail_color(self):
        ''' A bit of lighter color for the tail '''
        (r,g,b) = self.color
        return (min(255, r+70), min(255, g+70), min(255, b+70))

    def grow(self):
        new_tail = Tail(self, len(self.tail)+1)
        self.tail.append(new_tail)
        self.collidable_tail_group.add(new_tail)
        self.group.add(new_tail)
        self.score+=1

    def handle_input(self, command):
        self.direction = command

    def loose(self):
        self.dead = True
        self.score -= 1
        self.pause = 100

    def is_self_hit(self):
        ''' Did the snake hit itself '''
        hit = pygame.sprite.spritecollide(self, self.collidable_tail_group, False)
        return len(hit) > 0

    def update(self):
        #check hit:
        if self.pause > 0:
            if self.pause == 1:
                self.reset()
            self.pause -= 1
            return

        if self.direction == 'left':
            self.rect = self.rect.move([-SPEED, 0])
        elif self.direction == 'right':
            self.rect = self.rect.move([SPEED, 0])
        elif self.direction == 'up':
            self.rect = self.rect.move([0, -SPEED])
        elif self.direction == 'down':
            self.rect = self.rect.move([0, SPEED])

        self.positions.append( (self.rect.x, self.rect.y) ) #TODO this will run out of memory

        if self.rect.x < -HALF_BLOCK:
            self.rect.x = config.SCREEN_WIDTH + HALF_BLOCK
        elif self.rect.x > config.SCREEN_WIDTH + HALF_BLOCK:
            self.rect.x = -HALF_BLOCK
        if self.rect.y < -HALF_BLOCK:
            self.rect.y = config.SCREEN_HEIGHT + HALF_BLOCK
        elif self.rect.y > config.SCREEN_HEIGHT + HALF_BLOCK:
            self.rect.y = -HALF_BLOCK
        for t in self.tail:
            t.update()
