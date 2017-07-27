import sys, pygame
import server
from player import Player
from food import Food

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

def handle_input(player, action, players, player_group):
    if action == "register":
        new_player = register_player(player, players)
        if new_player:
            player_group.add(new_player)
        return
    if player not in players:
        print("WARN: unregistered player trying to perform action: " + action)
        return
    players[player].handle_input(action)

def handle_nonlocal_input(input, players, player_group):
    player, action = input.split("/")
    handle_input(player, action, players, player_group)

def handle_local_input(type, key, players, player_group):
    """ type === KEYDOWN or KEYUP """
    if key not in key_map:
        return #nothing to do here
    handle_input(LOCAL_PLAYER_NAME, key_map[key], players, player_group)

pygame.init()

size = width, height = 800, 600
BLACK = 0, 0, 0
clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)
players = {}

#We keep our sprites in groups to easily manage them
player_group = pygame.sprite.Group()

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()

server.start()

food = Food()
food.place_random()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server.stop()
            sys.exit()
        elif event.type == KEYDOWN or event.type == KEYUP:
            handle_local_input(event.type, event.key, players, player_group)
    while not server.q.empty():
        handle_nonlocal_input(server.q.get(), players, player_group)

    screen.fill(BLACK)
    #Check collisions
    players_ate = pygame.sprite.spritecollide(food, player_group, False)
    for p in players_ate:
        p.grow()
    if len(players_ate) > 0:
        food.place_random()

    #Add everything to the screen
    for key, p in players.iteritems():
        p.update()
        screen.blit(p.image, p.rect)
        for t in p.tail:
            screen.blit(t.image, t.rect)
        screen.blit(food.image, food.rect)
    pygame.display.flip()
    clock.tick(50) #Don't run faster then 50 fps
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
