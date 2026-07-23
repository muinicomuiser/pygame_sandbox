from abc import ABC, abstractmethod
from scipy.signal import convolve2d
import numpy as np


class BaseGrid(ABC):
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self._cells_array = np.zeros((rows, columns)).astype(np.uint8)

    @abstractmethod
    def get_neighbors(self, kernel):
        pass

    @abstractmethod
    def update(self, kernel, update_function):
        pass

    @abstractmethod
    def get_alive_array(self):
        pass

    @abstractmethod
    def set_alive_array(self, array):
        pass

    @abstractmethod
    def toggle_cell(self, position):
        pass

    @abstractmethod
    def clear(self):
        pass


class InfiniteGrid(BaseGrid):

    def get_neighbors(self, kernel):
        neighbors = convolve2d(self._cells_array, kernel, mode="same", boundary="wrap")
        return neighbors

    def update(self, kernel, rule, update_function):
        neighbors = self.get_neighbors(kernel)
        self._cells_array = update_function(self._cells_array, neighbors, rule)

    def get_alive_array(self):
        return self._cells_array

    def set_alive_array(self, array):
        self._cells_array = array

    def toggle_cell(self, position):
        column, row = position
        self._cells_array[row, column] ^= 1

    def clear(self):
        self._cells_array = np.zeros((self.rows, self.columns)).astype(np.uint8)


class ClosedGrid(BaseGrid):
    def get_neighbors(self, position):
        pass
