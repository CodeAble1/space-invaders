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

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(center = (400, 400))
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
        if keys[pygame.K_RIGHT]:
            self.rect.x += 3
        if keys[pygame.K_UP]:
            self.rect.y -= 3
        if keys[pygame.K_DOWN]:
            self.rect.y += 3
    
    def update(self):
        self.player_input()

#Initialization
player = pygame.sprite.GroupSingle()
player.add(Player())


# Event Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((0,0,0))
    player.draw(screen)
    player.update()

    pygame.display.update()
    clock.tick(FPS)
