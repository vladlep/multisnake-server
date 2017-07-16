import sys, pygame
import server
from player import Player

from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
    K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

LOCAL_PLAYER_NAME = 'berry'
key_map = {K_LEFT: 'left', K_UP: 'up', K_RIGHT: 'right', K_DOWN: 'down', K_RETURN: 'register'}

def register_player(name, players):
    if name in players:
        print("WARN: Player already exists")
        return
    new_player = Player(name, 0, 0) #TODO check if position is free
    players[name] = new_player
    return new_player

def handle_input(player, action, players):
    if action == "register":
        register_player(player, players)
        return
    if player not in players:
        print("WARN: unregistered player trying to perform action: " + action)
        return
    players[player].handle_input(action)

def handle_nonlocal_input(input, players):
    player, action = input.split("/")
    handle_input(player, action, players)

def handle_local_input(type, key, players):
    """ type === KEYDOWN or KEYUP """
    if key not in key_map:
        return #nothing to do here
    handle_input(LOCAL_PLAYER_NAME, key_map[key], players)

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
        elif event.type == KEYDOWN or event.type == KEYUP:
            handle_local_input(event.type, event.key, players)
    while not server.q.empty():
        handle_nonlocal_input(server.q.get(), players)

    screen.fill(black)
    for key, p in players.iteritems():
        p.update()
        screen.blit(p.image, p.rect)
    pygame.display.flip()
    clock.tick(50) #Don't run faster then 50 fps
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
