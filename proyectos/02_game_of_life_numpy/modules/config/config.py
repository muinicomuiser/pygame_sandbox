from dataclasses import dataclass
from enum import Enum
class COLORS(tuple, Enum):
    AMARILLO = (255, 255, 0)
    BLANCO = (255, 255, 255)
    BLANCO_INVIERNO = (255, 250, 240)
    NEGRO = (0, 0, 0)
    GRAFITO = (30, 30, 30)
    PLOMO = (90, 90, 90)
    GRIS = (170, 170, 170)
    CREMA = (240, 240, 120)
# Dataclass para configuraciones de una clase
@dataclass(frozen=True)
class Config:
    # Constantes de clase. Solo por convención. Mayúsculas para indicar que una propiedad es una constante.
    # Con frozen sí se vuelven inmutables
    TILESIZE: int = 4
    WIDTH: int = 1440
    HEIGHT: int = 720

    RAND_GENERATION_RANGE: float = 0.5
    FRAMERATE: int = 12

    BACKGROUND_COLOR: tuple = COLORS.NEGRO
    TILE_COLOR: tuple = COLORS.GRIS
    GRID_COLOR: tuple = COLORS.GRIS
    FONT_COLOR: tuple = (200, 200, 255)
    FONT_SIZE: int = 12

    RECORDINGS_DIR = "grabaciones"

    # Convierte una función en una propiedad. Para setters, getters y deleters
    @property
    def COLUMNS(self) -> int:
        return self.WIDTH // self.TILESIZE

    @property
    def ROWS(self) -> int:
        return self.HEIGHT // self.TILESIZE

def load_config() -> Config:
    return Config()
