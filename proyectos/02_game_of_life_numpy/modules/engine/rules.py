import numpy as np


class GameRules:
    @staticmethod
    def base_kernel():
        kernel = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1],
            ])
        return kernel
    @staticmethod
    def a_kernel():
        kernel = np.array([
            [1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [1, 0, 0, 0, 1],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 1],
            ])
        return kernel
    @staticmethod
    def b_kernel():
        kernel = np.array([
            [1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 1],
            ])
        return kernel
    @staticmethod
    def c_kernel():
        kernel = np.array([
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            ])
        return kernel