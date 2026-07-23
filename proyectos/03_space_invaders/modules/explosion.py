import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, images: dict[str, pygame.Surface]):
        pygame.sprite.Sprite.__init__(self)
        self.image_set = images
        self.image = images["explosion_1"]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.count = 0
        self.sprite_idx = 0

    def update(self):
        max_count = 3
        if self.sprite_idx >= 5 - 1 and self.count > max_count:
            self.kill()
            return
        elif self.sprite_idx < 5 - 1 and self.count > max_count:
            self.sprite_idx += 1
            self.count = 0
            self.image = self.__select_image(self.sprite_idx)
            return
        self.count += 1

        
    def __select_image(self, idx) ->  pygame.Surface:
        return self.image_set[f"explosion_{idx +1}"]
