# Tomado de https://github.com/hunar4321/particle-life/blob/main/particle_life.py
# Usuario https://github.com/hunar4321
# Y modificado para usar @jit()
from numba import jit
import numpy as np
import pygame
import random

atoms = []
window_size = 720
pygame.init()
window = pygame.display.set_mode((window_size, window_size))


def get_color(color_id):
    match color_id:
        case 0.0:
            return "white"
        case 1.0:
            return "red"
        case 2.0:
            return "green"


def draw(surface, x, y, color, size):
    for i in range(0, size):
        pygame.draw.circle(surface, color, (x, y), abs(size // 2))


def atom(x, y, c):
    return np.array([x, y, 0.0, 0.0, c])


def randomxy():
    return round(random.random() * window_size + 1)


def create(number, color):
    group = np.empty((number, 5))
    for i in range(number):
        new_atom = atom(randomxy(), randomxy(), color)
        group[i] = new_atom
        atoms.append((group[i]))
    return group


@jit(nopython=True)
def rule(atoms1, atoms2, g):
    for i in range(len(atoms1)):
        fx = 0.0
        fy = 0.0

        ax = atoms1[i, 0]
        ay = atoms1[i, 1]

        for j in range(len(atoms2)):
            bx = atoms2[j, 0]
            by = atoms2[j, 1]

            dx = ax - bx
            dy = ay - by
            d = (dx * dx + dy * dy) ** 0.5

            if 6 < d < 80:
                F = g / d
                fx += F * dx
                fy += F * dy
            elif 0 < d < 6:
                F = (g + 1) / d
                fx += F * dx
                fy += F * dy

        atoms1[i, 2] = (atoms1[i, 2] + fx) * 0.5  # vx
        atoms1[i, 3] = (atoms1[i, 3] + fy) * 0.5  # vy

        atoms1[i, 0] += atoms1[i, 2]  # x
        atoms1[i, 1] += atoms1[i, 3]  # y

        if atoms1[i, 0] <= 0 or atoms1[i, 0] >= window_size:
            atoms1[i, 2] *= -1
        if atoms1[i, 1] <= 0 or atoms1[i, 1] >= window_size:
            atoms1[i, 3] *= -1


yellow = create(2000, 0)
red = create(1000, 1)
blue = create(800, 2)

run = True
while run:
    window.fill(0)
    rule(red, red, -0.1)
    rule(red, yellow, -0.35)
    rule(blue, red, -0.3)
    rule(red, blue, 0.5)
    rule(yellow, blue, -0.35)
    rule(yellow, red, 0.35)
    rule(yellow, yellow, 0.1)
    for i in range(len(atoms)):
        color = get_color(atoms[i][4])
        draw(window, atoms[i][0], atoms[i][1], color, 8)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
exit()
