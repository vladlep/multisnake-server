import sys, pygame
import server
from player import Player


def handle_input(input, players):
    player, move = input.split("/")
    try:
        players[player].handle_input(move)
    except KeyError:
        new_player = Player(player, 0, 0)
        players[player] = new_player
        handle_input(input, players)


pygame.init()

size = width, height = 3*320, 3*240
speed = [2, 2]
black = 0, 0, 0
clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)
players = {
    1: Player(1, 10, 10),
    2: Player(2, 50, 50)
}

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()

server.start()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server.stop()
            sys.exit()
    while not server.q.empty():
        handle_input(server.q.get(), players)
        print(server.q.get()) #debug

    screen.fill(black)
    for key, p in players.iteritems():
        p.update()
        screen.blit(p.image, p.rect)
    pygame.display.flip()
    clock.tick(50) #Don't run faster then 50 fps
    pygame.display.set_caption("fps: " + str(clock.get_fps()))