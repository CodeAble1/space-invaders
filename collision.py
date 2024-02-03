import pygame

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