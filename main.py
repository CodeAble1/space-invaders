import pygame
import sys

pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
FPS = 60

# Setup
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()


# Event Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.time(FPS)
