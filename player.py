import pygame

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, screen_surface, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load("assets/pixel_ship_yellow.png").convert_alpha()
        self.rect = self.image.get_rect(center = (400, 400))
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 100
        self.timer = 60
        self.speed = 5
        self.screen_surface = screen_surface
        self.screen_height = screen_height
        self.screen_width = screen_width
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right <= self.screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top >= 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom <= self.screen_height:
            self.rect.y += self.speed

    def health_bar(self):
        damage_bar = pygame.Rect(self.rect.bottomleft[0], self.rect.bottomleft[1] + 10, self.rect.width, 10)
        health = pygame.Rect(self.rect.bottomleft[0], self.rect.bottomleft[1] + 10, self.health, 10)
        pygame.draw.rect(self.screen_surface, (255, 0, 0), damage_bar)
        pygame.draw.rect(self.screen_surface, (0, 255, 0), health)

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