import random
import sys
import numpy as np
import pygame
from modules.recorder.recorder import Recorder
from modules.spaceship import Spaceship
from modules.config import Config

class Game:
    def __init__(self, config: Config, recorder = None):
        pygame.init()
        self.config = config
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = True
        pygame.display.set_caption("Space Invaders")
        self.fps = self.config.FPS
        self.spaceship = Spaceship(self.config.WIDTH // 2, self.config.HEIGHT - 100, config.IMG_DIR)
        self.spaceship_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.time = 0
        self.recorder: Recorder = recorder
        self.stars = np.zeros((100, 4))
        self._create_stars()
        self.stars_velocity = 4

    def run(self):
        self.spaceship_group.add(self.spaceship)
        if self.recorder:
            self.recorder.init_record(self.screen.get_size())
        while self.running:
            self.clock.tick(self.fps)
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.spaceship.rect.left - self.spaceship.speed > 0:
                self.spaceship.move_left()
            if key[pygame.K_RIGHT] and self.spaceship.rect.right + self.spaceship.speed < self.config.WIDTH:
                self.spaceship.move_right()
            if key[pygame.K_UP] and self.spaceship.rect.top - self.spaceship.speed > 0:
                self.spaceship.move_up()
            if key[pygame.K_DOWN] and self.spaceship.rect.bottom + self.spaceship.speed < self.config.HEIGHT:
                self.spaceship.move_down()
            if key[pygame.K_SPACE]:
                new_bullet = self.spaceship.fire()
                if new_bullet:
                    self.bullet_group.add(new_bullet)

            # Update
            self.bullet_group.update()
            # Draw

            self.screen.fill((0, 0, 0))

            self.spaceship_group.draw(self.screen)
            self.bullet_group.draw(self.screen)


            bar_rect, bar_color = self.spaceship.get_health_bar()
            pygame.draw.rect(self.screen, rect=bar_rect, color=bar_color)
            self.time += 1
            self._draw_stars()
            pygame.display.update()
            if self.recorder:
                self.recorder.record_frame(self._image_frame())
        if self.recorder:
            self.recorder.release()
        pygame.quit()
        sys.exit()

    def _image_frame(self):
        frame = pygame.surfarray.array3d(self.screen)
        frame = np.transpose(frame, (1, 0, 2))
        return frame

    def _draw_stars(self):
        for star in self.stars:
            # star[1] += star[2]
            if star[1] > self.config.HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, self.config.WIDTH)
            if star[3] > 80 or star[3] < 20:
                star[2] *= -1
            star[3] += star[2]
            
            val = star[3]
            color = (val, val, val)

            pygame.draw.circle(self.screen, color, (star[0], star[1]), 1)

    def _create_stars(self):
        for star in self.stars:
            star[0] = random.randint(0, self.config.WIDTH)
            star[1] = random.randint(0, self.config.HEIGHT)
            # star[2] = random.randint(18, 20) / 3 # Velocidad
            # star[2] = random.randint(24, 26) / 3 # Velocidad
            star[2] = random.randint(3, 5) # Velocidad
            star[3] = random.randint(20, 80) # Brillo
