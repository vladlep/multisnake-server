import pygame
import config

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self.image = pygame.Surface( (config.SCREEN_WIDTH, 50) )
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        default_font = pygame.font.get_default_font()
        self.font = pygame.font.Font(default_font, 18)

    def update(self, players):
        text = ""
        for p in players.sprites():
            text += p.name + ": " + str(p.score) + "  "
        score = self.font.render(text, True, (250, 50, 50))
        self.image.fill( (0,0,0) )
        self.image.blit(score, (0, 0))
