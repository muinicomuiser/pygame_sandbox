import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img: pygame.Surface, limit_y=0, limit_x=0):
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
        bullet = Bullet(x, y, image)
        return bullet
