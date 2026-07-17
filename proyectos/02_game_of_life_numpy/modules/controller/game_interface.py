import sys
import cv2
from cv2.typing import MatLike
import numpy as np
import pygame
from modules.config.config import Config
from modules.engine.engine import BaseEngine
from modules.engine.recorder import Recorder

class GameInterface:
    def __init__(self, config: Config, engine: BaseEngine, recorder: Recorder):
        pygame.init()
        self.config = config
        self.engine = engine 
        self.running = True
        self.framerate = self.config.FRAMERATE
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", self.config.FONT_SIZE)
        self.quit_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.framerate_limiter = True
        self.show_metrics = False
        self.count = 0
        self.show_grid = False
        self.playing = True
        self.recorder = recorder
        self.recording = False
        self.caption = f"Game of Life - Playing" if self.playing else f"Game of Life - Paused"
        pygame.display.set_caption(self.caption)
    def run(self):
        while self.running:
            self.clock.tick(self.framerate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.caption = "Game of Life"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._mouse_events()

                if event.type == pygame.KEYDOWN:
                    self._key_events(event.key)
         
            if self.playing:
                self.engine.next_step()
                self.count += 1
            
            self.screen.fill(self.config.BACKGROUND_COLOR)
            if self.show_grid:
                self._draw_cells_and_grid_np_array_()
            else:
                # self._draw_cells_np_array_()
                self._draw_circular_cells_and_grid_np_array_()
            if self.show_metrics:
                self._render_metrics()
            pygame.display.flip()

            if self.recording:
                frame = self._image_frame()
                self.recorder.record_frame(frame)


            # Mover el cursor a la posición guardada
            print("\033[u", end="")
            # \033[K para limpiar lo que queda de la línea
            print(f"FPS: {int(self.clock.get_fps())} frames\033[K")
            print(f"STEPS: {self.count}\033[K", end="", flush=True)
            # Borrar lo que se escriba abajo
            print("\033[J", end="", flush=True) 
            # print(f"\rFPS: {int(self.clock.get_fps())} frames", end="", flush=True)
        
        
        self.recorder.release()
        pygame.quit()
        sys.exit()

    def _draw_cells_and_grid_np_array_(self):
        rows, columns = np.nonzero(self.engine.get_cells_array())
        for r, c in zip(rows, columns):
            x = (c * self.config.TILESIZE) + 1
            y = (r * self.config.TILESIZE) + 1
            pygame.draw.rect(self.screen, self.config.TILE_COLOR, (x, y, self.config.TILESIZE - 2, self.config.TILESIZE - 2))

    def _draw_circular_cells_and_grid_np_array_(self):
        rows, columns = np.nonzero(self.engine.get_cells_array())
        for r, c in zip(rows, columns):
            radio = self.config.TILESIZE // 2
            x = c * self.config.TILESIZE + radio
            y = r * self.config.TILESIZE + radio
            pygame.draw.circle(surface=self.screen, color=self.config.TILE_COLOR, radius=radio, center=(x, y))

    def _draw_cells_np_array_(self):
        rows, columns = np.nonzero(self.engine.get_cells_array())
        for r, c in zip(rows, columns):
            x = c * self.config.TILESIZE
            y = r * self.config.TILESIZE
            pygame.draw.rect(self.screen, self.config.TILE_COLOR, (x, y, self.config.TILESIZE, self.config.TILESIZE))

    def _render_metrics(self):
        char_x, char_y = 20, 20      
        alive_count = self.engine.get_alive_count()  
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, self.config.FONT_COLOR)
        fps_limit_text = self.font.render(f"FPS Limit: {int(self.framerate)}" if self.framerate_limiter else "FPS Limit: Off", True, self.config.FONT_COLOR)
        cells_count_text =  self.font.render(f"Cells count: {alive_count}", True, self.config.FONT_COLOR)
        steps_count_text =  self.font.render(f"Steps count: {self.count}", True, self.config.FONT_COLOR)
        self.screen.blit(fps_text, (char_x, char_y))
        self.screen.blit(fps_limit_text, (char_x, char_y + 20))
        self.screen.blit(cells_count_text, (char_x, char_y + 40))
        self.screen.blit(steps_count_text, (char_x, char_y + 60))

    def _mouse_events(self):
        x, y = pygame.mouse.get_pos()
        col = x // self.config.TILESIZE
        row = y // self.config.TILESIZE
        self.engine.toggle_pos((col, row)) 

    def _key_events(self, key):
        if key == pygame.K_SPACE:
            self.playing = not self.playing
            caption = f"Game of Life - Playing" if self.playing else f"Game of Life - Paused"
            if self.recording:
                self.caption = f"{caption} - Grabando"
            else:
                self.caption = caption
            pygame.display.set_caption(self.caption)
        if key == pygame.K_c:
            self.engine.clear()
            self.playing = False
            self.count = 0
        if key == pygame.K_g:
            self.engine.random_positions()    
            self.count = 0
        if key == pygame.K_r:
            self.recording = not self.recording   
            caption = f"Game of Life - Playing" if self.playing else f"Game of Life - Paused"
            if self.recording:
                self.recorder.init_record(self.screen.get_size())
                self.caption = f"{caption} - Grabando"
            else:
                if self.recorder:
                    self.recorder.release()
                self.caption = caption
            pygame.display.set_caption(self.caption)
        if key == pygame.K_m:
            self.show_metrics = not self.show_metrics   
        if key == pygame.K_l:
            self.show_grid = not self.show_grid
        if key == pygame.K_f:
            self.framerate_limiter = not self.framerate_limiter
            if self.framerate_limiter:
                self.framerate = self.config.FRAMERATE
            else:
                self.framerate = 0
        if key == pygame.K_KP_MINUS and self.framerate > 1 and self.framerate_limiter:
            self.framerate -= 1
        if key == pygame.K_KP_PLUS and self.framerate_limiter:
            self.framerate += 1        

    def _image_frame(self) -> MatLike:
        frame = pygame.surfarray.array3d(self.screen)
        frame = np.transpose(frame, (1, 0, 2))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)    
        return frame