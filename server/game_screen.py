import sys, pygame
import server

pygame.init()

size = width, height = 3*320, 3*240
speed = [2, 2]
black = 0, 0, 0
clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()

server.start()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server.stop()
            sys.exit()
    while not server.q.empty():
        print(server.q.get()) #TODO handle input here

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    clock.tick(500) #Don't run faster then 50 fps
    pygame.display.set_caption("fps: " + str(clock.get_fps()))