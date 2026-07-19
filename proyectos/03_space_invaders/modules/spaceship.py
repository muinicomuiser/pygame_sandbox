import pygame


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, images: dict[str, pygame.Surface], world_shape):
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

    def get_health_bar(self):
        x, y = self.rect.bottomleft
        bar_length = (self.rect.width // self.start_health) * self.health
        bar_rect = pygame.Rect(x, y + 10, bar_length, 5)
        bar_color = (60, 180, 255)
        return (bar_rect, bar_color)

    def fire(self):
        time = pygame.time.get_ticks()
        limit_x, limit_y = self.world_shape
        x, y = self.rect.centerx, self.rect.top
        if time - self.last_shot < self.cooldown:
            return None
        self.last_shot = time
        match(self.weapon_id):
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
        match(self.weapon_id):
            case 1:
                self.cooldown = 100    
            case 2:
                self.cooldown = 400    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img: pygame.Surface, limit_y = 0, limit_x = 0):
        pygame.sprite.Sprite.__init__(self)
        # self.width = 4
        # self.heigth = 12
        self.color = (255, 255, 255)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity_y = 10
        self.velocity_x = 0
        self.limit_y = limit_y
        self.limit_x = limit_x

    def update(self):
        if self.velocity_x != 0:
            new_x = self.rect.x + self.velocity_x
            if new_x < 0 or new_x > self.limit_x:
                self.kill()
            self.rect.x = new_x        
        new_y = self.rect.y - self.velocity_y
        if new_y < self.limit_y:
                self.kill()
        self.rect.y = new_y

    @staticmethod
    def base_bullet(x, y, image):
        bullet =  Bullet(x, y, image)
        return bullet