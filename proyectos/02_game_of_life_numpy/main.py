from modules.config.config import load_config
from modules.engine.engine import  GameOfLifeEngineNumpy
from modules.engine.grid import InfiniteGrid
from modules.controller.game_interface import GameInterface
from modules.engine.recorder import Recorder
from modules.engine.rules import GameRules

if __name__ == "__main__":
    config = load_config()
    grid = InfiniteGrid(config.COLUMNS, config.ROWS)
    kernel = GameRules.base_kernel()
    # kernel = GameRules.a_kernel()
    # kernel = GameRules.b_kernel()
    # kernel = GameRules.c_kernel()

    engine = GameOfLifeEngineNumpy(grid, kernel, config.RAND_GENERATION_RANGE)    
    recorder = Recorder(config.FRAMERATE, config.RECORDINGS_DIR)
    game = GameInterface(config, engine, recorder)
    game.run()
