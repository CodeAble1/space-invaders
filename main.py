import pygame
import sys
from random import randint

pygame.init()

# Constants
WIDTH,HEIGHT = 800, 600
FPS = 60
RUN = False

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
background = pygame.image.load("assets/background-black.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
enemy_timer = 60
shooting_timer = [80, 120, 160]
score = 0


# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/pixel_ship_yellow.png").convert_alpha()
        self.rect = self.image.get_rect(center = (400, 400))
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 100
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

    def health_bar(self):
        damage_bar = pygame.Rect(self.rect.bottomleft[0], self.rect.bottomleft[1] + 10, self.rect.width, 10)
        health = pygame.Rect(self.rect.bottomleft[0], self.rect.bottomleft[1] + 10, self.health, 10)
        pygame.draw.rect(screen, (255, 0, 0), damage_bar)
        pygame.draw.rect(screen, (0, 255, 0), health)

    def damage(self):
        self.health -= 10
    
    def reset(self):
        self.health = 100
        self.rect.center = (400, 400)

    def update(self):
        self.health_bar()
        self.player_input()
        self.timer -= 2

# Projectile
class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/pixel_laser_yellow.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
    
    def destroy(self):
        if self.rect.y < -200:
            self.kill()

    def update(self):
        self.destroy()
        self.rect.y -= 3
    

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        if self.type == 1:
            self.image = pygame.image.load("assets/pixel_ship_blue_small.png").convert_alpha()
        elif self.type == 2:
            self.image = pygame.image.load("assets/pixel_ship_green_small.png").convert_alpha()
        elif self.type == 3:
            self.image = pygame.image.load("assets/pixel_ship_red_small.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def destroy(self):
           if self.rect.y >= HEIGHT + 50:
            self.kill() 

    def update(self):
        self.destroy()
        self.rect.y += 1



# EnemyProjectiles
class EnemyProjectiles(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        self.x = x
        self.y = y
        if self.type == 1: 
            self.image = pygame.image.load("assets/pixel_laser_blue.png").convert_alpha()
        elif self.type == 2:
            self.image = pygame.image.load("assets/pixel_laser_green.png").convert_alpha()
        elif self.type == 3:
            self.image = pygame.image.load("assets/pixel_laser_red.png").convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def destroy(self):
           if self.rect.y >= HEIGHT + 50:
            self.kill() 

    def update(self):
        self.destroy()
        self.rect.y += 1.5

     
# Collisions
def ProjectileCollision(enemy_projectile, player_projectile):
    for sprite1 in enemy_projectile:
        for sprite2 in player_projectile:
            if pygame.sprite.collide_mask(sprite1, sprite2):
                enemy_projectile.remove(sprite1)
                player_projectile.remove(sprite2)
                return True

def PlayerCollision(enemy, player):
    for sprite1 in enemy:
        for sprite2 in player:
            if pygame.sprite.collide_mask(sprite1, sprite2):
                enemy.remove(sprite1)
                player.sprite.damage()
                return True
                
#Groups
player_group = pygame.sprite.GroupSingle()
player_projectile = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_projectile = pygame.sprite.Group()

ship = Player()



# Event Loop
while True:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)

    # Start Menu
    if not RUN:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            RUN = True
            ship.reset()
            score = 0
            player_group.add(ship)
    
        # Drawing 
        start_surface = font.render("Press SPACE to Start", False, (255, 255, 255))
        start_rect = start_surface.get_rect(center = (WIDTH // 2, HEIGHT // 2))

        prev_score_surface = font.render(f"Your Score was {score}", False, (255, 255, 255))
        prev_score_rect = prev_score_surface.get_rect( center = (WIDTH // 2, (HEIGHT// 2) - 100))


        # Update
        screen.blit(background, (0,0))
        screen.blit(start_surface, start_rect)
        screen.blit(prev_score_surface, prev_score_rect)
        pygame.display.update()
        

    # Game
    if RUN:        
        # Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and ship.timer <= 0:
            proj = PlayerProjectile(ship.rect.x, ship.rect.y)
            player_projectile.add(proj)
            ship.timer = 60

        

        # Enemy Logic
        if enemy_timer <= 0:
            enemy_ship = Enemy(randint(1, 3), randint(50, WIDTH-50), randint(-100, 0))
            enemy_group.add(enemy_ship)
            enemy_timer = 60
        
        for enemy in enemy_group.sprites():
            if shooting_timer[0] <= 0 and enemy.type == 1:
                enemy_proj = EnemyProjectiles(enemy.type, enemy.rect.centerx, enemy.rect.centery)
                enemy_projectile.add(enemy_proj)
                
            if shooting_timer[1] <= 0 and enemy.type == 2:
                enemy_proj = EnemyProjectiles(enemy.type, enemy.rect.centerx, enemy.rect.centery)
                enemy_projectile.add(enemy_proj)
            
            if shooting_timer[2] <= 0 and enemy.type == 3:
                enemy_proj = EnemyProjectiles(enemy.type, enemy.rect.centerx, enemy.rect.centery)
                enemy_projectile.add(enemy_proj)

        # Reset timers
        if shooting_timer[0] <= 0:
            shooting_timer[0] = 80
        if shooting_timer[1] <= 0:
            shooting_timer[1] = 120
        if shooting_timer[2] <= 0:
            shooting_timer[2] = 160
        
        # Collision
        ProjectileCollision(player_projectile, enemy_projectile)
        if ProjectileCollision(enemy_group, player_projectile):
            score += 1
        if PlayerCollision(enemy_group, player_group):
            score += 1
        if PlayerCollision(enemy_projectile, player_group):
            if player_group.sprite.health <= 0:
                RUN = False
                player_group.empty()
                enemy_group.empty()
                player_projectile.empty()
                enemy_projectile.empty()


        # Score
        score_surface = font.render(f"Score {score}", True, (255, 255, 255))
    
        # Drawing
        screen.blit(background, (0,0))
        screen.blit(score_surface, (20, 20))
        player_group.draw(screen)
        player_projectile.draw(screen)
        enemy_group.draw(screen)
        enemy_projectile.draw(screen)
    
        
        # Update
        player_projectile.update()
        enemy_projectile.update()
        player_group.update()
        enemy_group.update()
        pygame.display.update()
        
        enemy_timer -= 0.5
        for i, value in enumerate(shooting_timer):
            shooting_timer[i] -= 1

