import pygame

from modules.explosion import Explosion
from modules.projectile import AlienBullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, images: dict[str, pygame.Surface], world_shape: tuple[int, int], movement_range_x: int):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images["alien_base"]        
        self.alien_bullet_image = images["alien_bullet"]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.world_shape = world_shape
        self.move_counter = 0
        self.movement_range_x = movement_range_x - (self.rect.width // 2)
        self.velocity_y = 14
        self.velocity_x = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, bullets_group, explosion_group, reverse: bool):
        if reverse:
            self.velocity_x *= -1
            self.velocity_x += int(self.velocity_x > 0)
            self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x

        # self.move_counter += 1 * abs(self.velocity_x)
        # if abs(self.move_counter) > self.movement_range_x:
        #     self.velocity_x *= -1
        #     self.move_counter *= -1
        #     self.rect.y += self.velocity_y
        if pygame.sprite.spritecollide(self, bullets_group, True):
            x, y = self.rect.center
            explosion = Explosion(x, y, self.images)
            explosion_group.add(explosion)
            self.kill()            

    def fire(self):
        limit_x, limit_y = self.world_shape
        x, y = self.rect.centerx, self.rect.top        
        bullet = AlienBullet(x, y, self.alien_bullet_image, limit_y=limit_y, limit_x=limit_x)
        return {bullet}