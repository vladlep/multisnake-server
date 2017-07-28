import sys, pygame
import server
import config
from player import Player
from food import Food
from score import Score

from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
    K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

LOCAL_PLAYER_NAME = 'berry'
key_map = {K_LEFT: 'left', K_UP: 'up', K_RIGHT: 'right', K_DOWN: 'down', K_RETURN: 'register'}

def get_player(name, players):
    for p in players: #No dict :(
        if p.name == name:
            return p
    return None

def register_player(name, players):
    if get_player(name, players):
        print("WARN: Player already exists")
        return
    new_player = Player(name) #TODO check if position is free
    players.add(new_player)
    return new_player

def handle_input(name, action, players):
    if action == "register":
        register_player(name, players)
        return
    player = get_player(name, players)
    if not player:
        print("WARN: unregistered player trying to perform action: " + action)
        return
    player.handle_input(action)

def handle_nonlocal_input(input, players):
    name, action = input.split("/")
    handle_input(name, action, players)

def handle_local_input(type, key, players):
    """ type === KEYDOWN or KEYUP """
    if key not in key_map:
        return #nothing to do here
    handle_input(LOCAL_PLAYER_NAME, key_map[key], players)

pygame.mixer.pre_init(44100, -16, 1, 512) #to prevent lag
pygame.init()
pygame.mixer.init()

size = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
BLACK = 0, 0, 0
clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)
players = pygame.sprite.Group()

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

score = Score()

#Sounds:
eat_sound = pygame.mixer.Sound("assets/audio/coin.wav")
die_sound = pygame.mixer.Sound("assets/audio/pixel_death.wav")

while 1:
    ######### Handle input ############
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server.stop()
            sys.exit()
        elif event.type == KEYDOWN or event.type == KEYUP:
            handle_local_input(event.type, event.key, players)
    while not server.q.empty():
        handle_nonlocal_input(server.q.get(), players)

    ############ Collisions ############
    #Check Food
    players_ate = pygame.sprite.spritecollide(food, players, False)
    for p in players_ate:
        p.grow()
        eat_sound.play()
    if len(players_ate) > 0:
        food.place_random()
    #Check self hits:
    for p in players.sprites():
        if not p.dead and p.is_self_hit():
            p.loose()
            die_sound.play(maxtime=1000)
    #Check hits with every other snake
    everything = pygame.sprite.Group()
    for p in players.sprites():
        everything.add(p.get_group())
    for p in players.sprites():
        if not p.dead:
            everything.remove(p.get_group()) # Remove self
            if len(pygame.sprite.spritecollide(p, everything, False, False)) > 0:
                print(p.name + " got hit!")
                p.loose()
                die_sound.play(maxtime=1000)
            everything.add(p.get_group()) # Add self

    ########## Adding to the screen ###########
    screen.fill(BLACK)
    screen.blit(score.image, score.rect)

    score.update(players)
    for p in players.sprites():
        p.update()
        screen.blit(p.image, p.rect)
        for t in p.tail:
            screen.blit(t.image, t.rect)

    screen.blit(food.image, food.rect)

    pygame.display.flip()
    clock.tick(50) #Don't run faster then 50 fps
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
