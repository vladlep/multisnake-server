import pygame

SPEED = 3
BLOCK_SIZE = 30
BETWEEN_SIZE = 5

class Tail(pygame.sprite.Sprite):
    def __init__(self, player, nr):
        self.player = player
        self.nr = nr
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(self.player.get_tail_color())
        self.rect = self.image.get_rect()
        #self.rect.x = -nr * BLOCK_SIZE - nr * BETWEEN_SIZE + self.player.rect.x #, 0])
        #self.rect.y = self.player.rect.y


    def update(self):
        self.rect.x, self.rect.y = self.player.get_position_behind(self.nr)
