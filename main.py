import pygame
import sys
from random import randint

pygame.init()

# Constants
WIDTH,HEIGHT = 800, 600
FPS = 60

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
enemy_timer = 60

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/pixel_ship_yellow.png").convert_alpha()
        self.rect = self.image.get_rect(center = (400, 400))
        self.timer = 60
        self.speed = 5
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right <= WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top >= 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom <= HEIGHT:
            self.rect.y += self.speed

    def update(self):
        self.player_input()
        self.timer -= 2

# Projectile
class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/pixel_laser_yellow.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.rect.y -= 3
        if self.rect.y < -200:
            self.kill()

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, option, x, y):
        super().__init__()
        if option == 1:
            self.image = pygame.image.load("assets/pixel_ship_blue_small.png").convert_alpha()
        elif option == 2:
            self.image = pygame.image.load("assets/pixel_ship_green_small.png").convert_alpha()
        elif option == 3:
            self.image = pygame.image.load("assets/pixel_ship_red_small.png").convert_alpha()
        self.rect = self.image.get_rect(center =(x, y))

    def update(self):
        self.rect.y += 2

        if self.rect.y >= HEIGHT + 50:
            self.kill()

#Groups
player = pygame.sprite.GroupSingle()
player_projectile = pygame.sprite.Group()
enemy = pygame.sprite.Group()

ship = Player()
player.add(ship)


# Event Loop
while True:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and ship.timer <= 0:
        proj = PlayerProjectile(ship.rect.x, ship.rect.y)
        player_projectile.add(proj)
        ship.timer = 60

    if enemy_timer <= 0:
        enemy_ship = Enemy(randint(1, 3), randint(20, WIDTH-20), randint(-100, 0))
        enemy.add(enemy_ship)
        enemy_timer = 60
    
    # Drawing
    screen.fill((0,0,0))
    player.draw(screen)
    player_projectile.draw(screen)
    enemy.draw(screen)
  
    
    # Update
    player_projectile.update()
    player.update()
    enemy.update()
    pygame.display.update()
    
    clock.tick(FPS)
    enemy_timer -= 1
