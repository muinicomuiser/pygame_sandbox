import pygame

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, img_dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir / "nave v3.png").convert_alpha() # convert_alpha para preservar transparencia de png
        self.bullet_image = pygame.image.load(img_dir / "bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 6
        self.start_health = 4
        self.health = self.start_health 
        self.last_shot = pygame.time.get_ticks()
        self.cooldown = 300

    def get_x(self):
        return self.rect.x
    
    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed
    
    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def get_health_bar(self):
        x, y = self.rect.bottomleft
        bar_length = (self.rect.width // self.start_health) * self.health
        bar_rect = pygame.Rect(x, y + 10, bar_length, 5)
        bar_color = (60, 180, 255)
        return (bar_rect, bar_color)

    def fire(self):
        time = pygame.time.get_ticks()

        if time - self.last_shot > self.cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_image)
            self.last_shot = time
            return bullet


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img: pygame.Surface, limit_y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.width = 4
        self.heigth = 12
        self.color = (255, 255, 255)
        # self.image = pygame.Surface((self.width, self.heigth))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        # self.image.fill(self.color)
        self.velocity = 10
        self.limit_y = limit_y

    def update(self):
        if self.rect.y > 0:
            self.rect.y -= self.velocity
        else:
            self.kill()
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 3)
