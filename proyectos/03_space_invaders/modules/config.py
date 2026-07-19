from enum import Enum
import logging
from pathlib import Path
import sys


class COLORS(tuple, Enum):
    AMARILLO = (255, 255, 0)
    BLANCO = (255, 255, 255)
    BLANCO_INVIERNO = (255, 250, 240)
    NEGRO = (0, 0, 0)
    GRAFITO = (30, 30, 30)
    CREMA = (240, 240, 120)
    CIAN = (200, 200, 255)


class SCREEN_SIZES(tuple, Enum):

    IG_REEL = (1080, 1920)  # 9:16
    """Proporción: 9:16"""

    IG_POST = (1080, 1440)  # 3:4
    """Proporción: 3:4"""

    SQUARE_1080 = (1080, 1080)
    SQUARE_720 = (720, 720)

    SD = (640, 480)  # 4:3
    """Proporción: 4:3"""

    QHD = (960, 540)  # 16:9
    """Proporción: 16:9"""

    HD = (1280, 720)  # 16:9
    """Proporción: 16:9"""

    FHD = (1920, 1080)  # 16:9
    """Proporción: 16:9"""

    VGA = (640, 480)  # 4:3
    """Proporción: 4:3"""

    SVGA = (800, 600)  # 4:3
    """Proporción: 4:3"""

    SD_VERT = (480, 640)  # 3:4
    """Proporción: 3:4"""

    QHD_VERT = (540, 960)  # 9:16
    """Proporción: 9:16"""

    HD_VERT = (720, 1280)  # 9:16
    """Proporción: 9:16"""

    FHD_VERT = (1080, 1920)  # 9:16
    """Proporción: 9:16"""

    SVGA_VERT = (600, 800)  # 3:4
    """Proporción: 3:4"""

    VGA_VERT = (480, 640)  # 3:4
    """Proporción: 3:4"""


class Config:
    WIDTH, HEIGHT = SCREEN_SIZES.SVGA_VERT
    FPS: int = 30
    BACKGROUND_COLOR: tuple = COLORS.NEGRO
    GRID_COLOR: tuple = COLORS.NEGRO
    FONT_COLOR: tuple = COLORS.CIAN
    FONT_SIZE: int = 12
    PROJECT_ROOT = Path(sys.argv[0]).resolve().parent
    IMG_DIR = PROJECT_ROOT / "img"
    CAPTURAS_DIR = PROJECT_ROOT / "capturas"
    ASSETS_LIST = {
        ("spaceship_base", "nave v3.png"),
        ("bullet_base", "bullet.png"),
    }


def load_config(args=None):
    config = Config()
    if args is None:
        return Config()

    if getattr(args, "fps", None) is not None:
        fps = max(1, min(args.fps, 144))
        if args.fps < 1 or args.fps > 144:
            logging.warning(
                f"FPS solicitado ({args.fps}) está fuera del rango (1 - 144). Se ajustó el valor a {fps}"
            )
        config.FPS = fps

    return config
