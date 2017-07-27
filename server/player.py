import pygame
import util
import config

from tail import Tail


SPEED = 3
BLOCK_SIZE = 30
HALF_BLOCK = 0.5 * BLOCK_SIZE

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
        self.score = 0
        self.pause = 0

        self.direction = ''
        self.tail = [ Tail(self, 1) ]
        self.tail_group = pygame.sprite.Group() #Everything except the first tail (because you will hit it anyways on turns)
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
        new_tail = Tail(self, len(self.tail)+1)
        self.tail.append(new_tail)
        self.tail_group.add(new_tail)
        self.score+=1

    def handle_input(self, command):
        self.direction = command

    def update(self):
        #check hit:
        if self.pause > 0:
            self.pause -= 1
            return

        hit = pygame.sprite.spritecollide(self, self.tail_group, False)
        if len(hit) > 0:
            self.score -= 1
            self.pause = 10

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
