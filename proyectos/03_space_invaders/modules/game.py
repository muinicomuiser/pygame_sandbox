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
        self.spaceship_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.time = 0
        self.recorder: Recorder = recorder
        self.stars = np.zeros((300, 4))
        self._create_stars()
        # self.stars_velocity = 4

        self.assets = self._init_assets()
        self.spaceship = Spaceship(self.config.WIDTH // 2, self.config.HEIGHT - 100, self.assets, (self.config.WIDTH, self.config.HEIGHT))

    def run(self):
        self.spaceship_group.add(self.spaceship)
        if self.recorder:
            self.recorder.init_record(self.screen.get_size())
        while self.running:
            self.clock.tick(self.fps)
            self.time += 1
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.spaceship.move_left()
            if key[pygame.K_RIGHT]:
                self.spaceship.move_right()
            if key[pygame.K_UP]:
                self.spaceship.move_up()
            if key[pygame.K_DOWN]:
                self.spaceship.move_down()
            if key[pygame.K_SPACE]:
                bullets = self.spaceship.fire()
                if bullets:
                    self.bullet_group.add(bullets)
            if key[pygame.K_1]:
                self.spaceship.set_weapon(1)
            if key[pygame.K_2]:
                self.spaceship.set_weapon(2)

            # Update
            self.bullet_group.update()
            # Draw

            self.screen.fill((0, 0, 0))
            self._draw_stars()

            self.spaceship_group.draw(self.screen)
            self.bullet_group.draw(self.screen)


            bar_rect, bar_color = self.spaceship.get_health_bar()
            pygame.draw.rect(self.screen, rect=bar_rect, color=bar_color)
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
            if star[1] > self.config.HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, self.config.WIDTH)
            if star[3] > 120 or star[3] < 20:
                star[2] *= -1
            star[3] += star[2]
            
            val = star[3]
            color = (val, val, val)

            # pygame.draw.circle(self.screen, color, (star[0], star[1]), 1)
            pygame.draw.rect(self.screen, color, (star[0], star[1], 1, 1))

    def _create_stars(self):
        for star in self.stars:
            star[0] = random.randint(0, self.config.WIDTH)
            star[1] = random.randint(0, self.config.HEIGHT)
            star[2] = random.randint(3, 6) # Pasos de variación de brillo
            star[3] = random.randint(20, 120) # Brillo inicial

    def _init_assets(self):
        assets = {}
        for name, file_name in self.config.ASSETS_LIST:
            assets[name] = pygame.image.load(self.config.IMG_DIR / file_name).convert_alpha() 
        return assets