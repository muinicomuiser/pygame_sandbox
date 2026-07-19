import argparse
import logging

from modules.game import Game
from modules.config import load_config
from modules.recorder.recorder import Recorder

def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Juego Space Invaders"
    )
    parser.add_argument("-r", "--record", help="graba la ejecución",
                    action="store_true")
    parser.add_argument("-f", "--fps", help="modifica los fps del juego (rango entre 1 y 144)",
                    type=int, required=False)
    args = parser.parse_args()


    config = load_config(args)
    recorder = (
        Recorder(config.FPS, config.CAPTURAS_DIR, "space_invaders")
        if args.record
        else None
    )
    game = Game(config, recorder) # Graba solo si recorder es distinto a None

    game.run()

if __name__ == "__main__":
    main()