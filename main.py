import pygame
import sys
from random import randint
from player import Player, PlayerProjectile
from enemy import Enemy, EnemyProjectiles
from collision import PlayerCollision, ProjectileCollision
from config import RUN, WIDTH, HEIGHT, FPS, ENEMY_TIMER, SHOOTING_TIMER

pygame.init()

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
background = pygame.image.load("assets/background-black.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
score = 0
             
#Groups
player_group = pygame.sprite.GroupSingle()
player_projectile = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_projectile = pygame.sprite.Group()
ship = Player(screen, WIDTH, HEIGHT)


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
        if ENEMY_TIMER <= 0:
            enemy_ship = Enemy(randint(1, 3), randint(50, WIDTH-50), randint(-100, 0), HEIGHT)
            enemy_group.add(enemy_ship)
            ENEMY_TIMER = 60
        
        for enemy in enemy_group.sprites():
            if SHOOTING_TIMER[0] <= 0 and enemy.type == 1:
                enemy_proj = EnemyProjectiles(enemy.type, enemy.rect.centerx, enemy.rect.centery, HEIGHT)
                enemy_projectile.add(enemy_proj)
                
            if SHOOTING_TIMER[1] <= 0 and enemy.type == 2:
                enemy_proj = EnemyProjectiles(enemy.type, enemy.rect.centerx, enemy.rect.centery, HEIGHT)
                enemy_projectile.add(enemy_proj)
            
            if SHOOTING_TIMER[2] <= 0 and enemy.type == 3:
                enemy_proj = EnemyProjectiles(enemy.type, enemy.rect.centerx, enemy.rect.centery, HEIGHT)
                enemy_projectile.add(enemy_proj)

        # Reset timers
        if SHOOTING_TIMER[0] <= 0:
            SHOOTING_TIMER[0] = 80
        if SHOOTING_TIMER[1] <= 0:
            SHOOTING_TIMER[1] = 120
        if SHOOTING_TIMER[2] <= 0:
            SHOOTING_TIMER[2] = 160
        
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
        
        ENEMY_TIMER -= 0.5
        for i, value in enumerate(SHOOTING_TIMER):
            SHOOTING_TIMER[i] -= 1

