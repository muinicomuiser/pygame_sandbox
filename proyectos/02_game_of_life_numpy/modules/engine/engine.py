import numpy as np

from modules.engine.grid import BaseGrid
from modules.engine.rules import GameRules

from abc import ABC, abstractmethod

class BaseEngine(ABC):
    def __init__(self, grid, kernel, random_range = 0.1):
        self.grid: BaseGrid = grid
        self.random_range = random_range
        self.random_generator = np.random.default_rng()
        self.random_positions()
        self.kernel = kernel
    @abstractmethod
    def random_positions(self):
        pass

    @abstractmethod
    def toggle_pos(self, position):
        pass

    @abstractmethod
    def next_step(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def get_cells_array(self):
        pass

    @abstractmethod
    def get_alive_count(self):
        pass

class GameOfLifeEngineNumpy(BaseEngine):
    def random_positions(self):
        random_array = self.random_generator.choice([0, 1], size=(self.grid.rows, self.grid.columns), p=[1 - self.random_range, self.random_range]).astype(np.uint8)
        self.grid.set_alive_array(random_array)

    def toggle_pos(self, position):
        self.grid.toggle_cell(position)

    def next_step(self):
        self.grid.update(self.kernel, rule_update_function)

    def clear(self):
        self.grid.clear()

    def get_cells_array(self):
        return self.grid.get_alive_array()

    def get_alive_count(self):
        return np.count_nonzero(self.get_cells_array())

def rule_update_function(array, neighbors):
    return ((neighbors == 3) | (array & (neighbors == 2))).astype(np.uint8)
    