import pygame
from modules.projectile import Bullet


class Spaceship(pygame.sprite.Sprite):
    def __init__(
        self, x, y, images: dict[str, pygame.Surface], world_shape: tuple[int, int]
    ):
        pygame.sprite.Sprite.__init__(self)
        self.image = images["spaceship_base"]
        self.bullet_image = images["bullet_base"]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 6
        self.start_health = 4
        self.health = self.start_health
        self.last_shot = pygame.time.get_ticks()
        self.cooldown = 100
        self.world_shape = world_shape
        self.weapon_id = 1
        self.weapons_list = {1, 2}
        self.set_weapon(1)
        # self.mask = pygame.mask.from_surface(self.image)

    def get_x(self):
        return self.rect.x

    def move_left(self):
        if self.rect.left - self.speed > 0:
            self.rect.x -= self.speed

    def move_right(self):
        if self.rect.right + self.speed < self.world_shape[0]:
            self.rect.x += self.speed

    def move_up(self):
        if self.rect.top - self.speed > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom + self.speed < self.world_shape[1]:
            self.rect.y += self.speed

    ## Esto puedo pasarlo a la función de update, para que se haga el cálculo de las dimensiones solo al colisionar
    def get_health_bar(self):
        x, y = self.rect.bottomleft
        bar_length = (self.rect.width // self.start_health) * self.health
        damage_bar_rect = pygame.Rect(x, y + 10, self.rect.width - 2, 5)
        damage_bar_color = (255, 60, 30)
        bar_rect = pygame.Rect(x, y + 10, bar_length, 5)
        bar_color = (60, 120, 255)
        return (damage_bar_rect, damage_bar_color, bar_rect, bar_color)

    def update(self, enemies_bullet_group: pygame.sprite.Group):
        if pygame.sprite.spritecollide(self, enemies_bullet_group, True, pygame.sprite.collide_mask):
            self.health -=1

    def fire(self):
        time = pygame.time.get_ticks()
        limit_x, limit_y = self.world_shape
        x, y = self.rect.centerx, self.rect.top
        if time - self.last_shot < self.cooldown:
            return None
        self.last_shot = time
        match (self.weapon_id):
            case 1:
                bullet = Bullet(x, y, self.bullet_image)
                return {bullet}
            case 2:
                bullet = Bullet(x, y, self.bullet_image, limit_x=limit_x)
                bullet2 = Bullet(x, y, self.bullet_image, limit_x=limit_x)
                bullet2.velocity_x = 2
                bullet3 = Bullet(x, y, self.bullet_image, limit_x=limit_x)
                bullet3.velocity_x = -2
                return {bullet, bullet2, bullet3}

    def set_weapon(self, id: int):
        if id in self.weapons_list and self.weapon_id != id:
            self.weapon_id = id
        match (self.weapon_id):
            case 1:
                self.cooldown = 300
            case 2:
                self.cooldown = 700