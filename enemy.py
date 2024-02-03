import pygame

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, x, y, screen_height):
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
        self.screen_height = screen_height

    def destroy(self):
           if self.rect.y >= self.screen_height + 50:
            self.kill() 

    def update(self):
        self.destroy()
        self.rect.y += 1



# EnemyProjectiles
class EnemyProjectiles(pygame.sprite.Sprite):
    def __init__(self, type, x, y, screen_height):
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
        self.screen_height = screen_height

    def destroy(self):
           if self.rect.y >= self.screen_height + 50:
            self.kill() 

    def update(self):
        self.destroy()
        self.rect.y += 1.5
