from collections import Counter
import sys
import pygame
from enum import Enum
import random


# Colores
class COLORS(tuple, Enum):
    AMARILLO = (255, 255, 0)
    BLANCO = (255, 255, 255)
    BLANCO_INVIERNO = (255, 250, 240)
    NEGRO = (0, 0, 0)
    GRAFITO = (30, 30, 30)
    CREMA = (240, 240, 120)


# Constantes
TILESIZE: int = 20
WIDTH, HEIGHT = 1440, 1080
RAND_GENERATION_RANGE: float = 0.06
FRAMERATE: int = 15
BACKGROUND_COLOR: tuple = COLORS.NEGRO
TILE_COLOR: tuple = COLORS.BLANCO
GRID_COLOR: tuple = COLORS.NEGRO
FONT_COLOR: tuple = (200, 200, 255)
FONT_SIZE: int = 12
COLUMNS = WIDTH // TILESIZE
ROWS = HEIGHT // TILESIZE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def main():
    running = True
    playing = True
    positions = random_positions()
    steps_count = 0
    show_grid = False
    show_metrics = False
    framerate = FRAMERATE
    limit_framerate = True
    pygame.display.set_caption("Game of Life")

    # Guardar la posición del cursor en la terminal
    print("\033[s", end="")

    while running:
        clock.tick(framerate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Mouse para cambiar estado de una célula
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILESIZE
                row = y // TILESIZE
                toggle_pos((col, row), positions)
            if event.type == pygame.KEYDOWN:
                key = event.key
                # Espacio para pausar
                if key == pygame.K_SPACE:
                    playing = not playing
                    caption = f"Game of Life" if playing else f"Game of Life - Paused"
                    pygame.display.set_caption(caption)
                # Tecla C para limpiar la pantalla
                if key == pygame.K_c:
                    positions = set()
                    playing = False
                    steps_count = 0
                # Tegla G para generar posiciones aleatorias
                if key == pygame.K_g:
                    positions = random_positions()
                    steps_count = 0
                # Tecla M para mostrar métricas
                if key == pygame.K_m:
                    show_metrics = not show_metrics
                # Tecla L para dibujar las líneas de la grilla
                if key == pygame.K_l:
                    show_grid = not show_grid
                # Tecla F para limitar los fps
                if key == pygame.K_f:
                    limit_framerate = not limit_framerate
                    if limit_framerate:
                        framerate = FRAMERATE
                    else:
                        framerate = 0
                # Teclas + y - para cambiar el límite de fps
                if key == pygame.K_KP_MINUS and framerate > 1:
                    framerate -= 1
                if key == pygame.K_KP_PLUS:
                    framerate += 1
        if playing:
            positions = next_step(positions)
            steps_count += 1
        screen.fill(BACKGROUND_COLOR)
        if show_grid:
            # draw_grid(screen)
            draw_cells_and_grid(screen, positions)
        else:
            draw_cells(screen, positions)
        if show_metrics:
            state = {
                "steps_count": steps_count,
                "framerate": framerate,
                "limit_framerate": limit_framerate,
                "cells_count": len(positions),
                "fps": int(clock.get_fps()),
            }
            draw_metrics(screen, state)
        pygame.display.flip()

        # Mover el cursor a la posición guardada
        print("\033[u", end="")
        # \033[K para limpiar lo que queda de la línea
        print(f"FPS: {int(clock.get_fps())} frames\033[K")
        print(f"STEPS: {steps_count}\033[K", end="", flush=True)
        # Borrar lo que se escriba abajo
        print("\033[J", end="", flush=True)

    pygame.quit()
    sys.exit()


def draw_cells(screen, positions):
    for position in positions:
        col, row = position
        top_left = (col * TILESIZE, row * TILESIZE)
        pygame.draw.rect(screen, TILE_COLOR, (*top_left, TILESIZE, TILESIZE))


def draw_cells_and_grid(screen, positions):
    for position in positions:
        col, row = position
        top_left = (col * TILESIZE + 1, row * TILESIZE + 1)
        pygame.draw.rect(screen, TILE_COLOR, (*top_left, TILESIZE - 2, TILESIZE - 2))


def draw_grid(screen):
    for col in range(0, COLUMNS):
        pygame.draw.line(
            screen, GRID_COLOR, (col * TILESIZE, 0), (col * TILESIZE, ROWS * TILESIZE)
        )
    for row in range(ROWS):
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, row * TILESIZE),
            (COLUMNS * TILESIZE, row * TILESIZE),
        )


def draw_metrics(screen, state):
    pygame_font = pygame.font.SysFont("Arial", FONT_SIZE)
    char_x, char_y = 20, 20
    fps_text = pygame_font.render(f"FPS: {state["fps"]}", True, FONT_COLOR)
    fps_limit_text = pygame_font.render(
        (
            f"FPS Limit: {int(state["framerate"])}"
            if state["limit_framerate"]
            else "FPS Limit: Off"
        ),
        True,
        FONT_COLOR,
    )
    cells_count_text = pygame_font.render(
        f"Cells count: {state["cells_count"]}", True, FONT_COLOR
    )
    steps_count_text = pygame_font.render(
        f"Steps count: {state["steps_count"]}", True, FONT_COLOR
    )
    screen.blit(fps_text, (char_x, char_y))
    screen.blit(fps_limit_text, (char_x, char_y + 20))
    screen.blit(cells_count_text, (char_x, char_y + 40))
    screen.blit(steps_count_text, (char_x, char_y + 60))


def random_positions():
    new_positions = set()
    for column in range(0, COLUMNS):
        for row in range(0, ROWS):
            random_bool = random.random() < RAND_GENERATION_RANGE
            if random_bool:
                new_positions.add((column, row))
    return new_positions


def toggle_pos(position, positions):
    if position in positions:
        positions.remove(position)
    else:
        positions.add(position)


def get_neighbors_infinite_grid(position):
    x, y = position
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            # neig_x = x + dx if (x + dx >= 0 and x + dx < COLUMNS) else ((COLUMNS - 1) if x + dx < 0 else 0)
            # neig_y = y + dy if (y + dy >= 0 and y + dy < ROWS) else ((ROWS - 1) if y + dy < 0 else 0)
            # a%b = a - (a//b) x b
            neig_x = (x + dx) % COLUMNS
            neig_y = (y + dy) % ROWS
            neighbors.append((neig_x, neig_y))
    return neighbors


def get_neighbors_closed_grid(position):
    x, y = position
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx == COLUMNS:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy == ROWS:
                continue
            if dx == 0 and dy == 0:
                continue
            neighbors.append((x + dx, y + dy))
    return neighbors


def next_step(positions):
    neighbor_counts = Counter()
    for x, y in positions:
        neighbors = get_neighbors_infinite_grid((x, y))
        for nx, ny in neighbors:
            neighbor_counts[(nx, ny)] += 1

    next_gen = {pos for pos, count in neighbor_counts.items() if count == 3}
    next_gen.update({pos for pos in positions if neighbor_counts[pos] == 2})
    return next_gen


if __name__ == "__main__":
    main()
