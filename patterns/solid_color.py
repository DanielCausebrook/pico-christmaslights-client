from typing import Optional

from colors import Color
from pattern import LightPattern
from palette import Palette


class SolidColorPattern(LightPattern):
    color: Optional[Color]

    def __init__(self, num_pixels, color: Optional[Color] = None):
        super().__init__(num_pixels)
        self.color = color

    def get_name(self):
        return 'Solid Color'

    def do_main_loop(self, t: float, delta_t: float, palette: Palette):
        color = self.color if self.color is not None else palette.primary
        for i in range(self.num_pixels):
            self.set_pixel(i, color)
