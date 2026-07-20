import random

import pygame

from modules.projectile import AlienBullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, images: dict[str, pygame.Surface], world_shape: tuple[int, int], movement_range_x: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = images["alien_base"]        
        self.alien_bullet_image = images["alien_bullet"]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.world_shape = world_shape
        self.move_counter = 0
        self.movement_range_x = movement_range_x - (self.rect.width // 2)
        self.velocity_y = 10
        self.velocity_x = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.velocity_x
        self.move_counter += 1 * abs(self.velocity_x)
        if abs(self.move_counter) > self.movement_range_x:
            self.velocity_x *= -1
            self.move_counter *= -1
            self.rect.y += self.velocity_y

    def fire(self):
        limit_x, limit_y = self.world_shape
        x, y = self.rect.centerx, self.rect.top        
        bullet = AlienBullet(x, y, self.alien_bullet_image, limit_y=limit_y, limit_x=limit_x)
        return {bullet}