import numpy as np


class GameRules:
    @staticmethod
    def rule_base():
        return ((3, 3), (2, 3))

    @staticmethod
    def rule_h():
        return ((2, 2), (34, 34))
    
    @staticmethod
    def rule_bugs():
        return ((34, 45), (37, 58))


    @staticmethod
    def base_kernel():
        kernel = np.array(
            [
                [1, 1, 1],
                [1, 0, 1],
                [1, 1, 1],
            ]
        )
        return kernel
    @staticmethod
    def h_kernel():
        kernel = np.array(
            [
                [1, 0, 1],
                [1, 1, 1],
                [1, 0, 1],
            ]
        )
        return kernel

    @staticmethod
    def a_kernel():
        kernel = np.array(
            [
                [1, 0, 0, 0, 0],
                [0, 0, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 0, 1],
            ]
        )
        return kernel

    @staticmethod
    def b_kernel():
        kernel = np.array(
            [
                [1, 0, 0, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 0, 1],
            ]
        )
        return kernel

    @staticmethod
    def c_kernel():
        kernel = np.array(
            [
                [1, 1, 1, 1, 1],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0],
            ]
        )
        return kernel
    
    @staticmethod
    def bugs_kernel():
        kernel = np.ones((11, 11))
        return kernel
    