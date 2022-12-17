import colorsys
from typing import Tuple


class Palette:
    primary: Tuple[float, float, float]
    secondary: Tuple[float, float, float]
    accent: Tuple[float, float, float]

    def __init__(self, primary=None, secondary=None, accent=None):
        self.primary = primary if primary is not None else colorsys.hsv_to_rgb(0.6, 1, 1)
        self.secondary = secondary if secondary is not None else colorsys.hsv_to_rgb(0.85, 1, 1)
        self.accent = accent if accent is not None else colorsys.hsv_to_rgb(0, 0, 1)
