import math

from LightPattern import LightPattern
from mathfun import rgb_interp, smoothstep
from palette import Palette


class CandyStripesPattern(LightPattern):
    width: int
    speed: float

    def __init__(self, num_pixels, width: int, speed: float = 8):
        super().__init__(num_pixels)

        self.width = width
        self.speed = speed

    def get_name(self):
        return 'Candy Stripes'

    def do_main_loop(self, t: float, delta_t: float, palette: Palette):
        for p in range(self.num_pixels):
            bar_pos = (p - t * self.speed) % (self.width * 2)
            amount = smoothstep(0, 1.5, bar_pos) - smoothstep(self.width, self.width + 1.5, bar_pos)
            color_rgb = rgb_interp(palette.primary, palette.secondary, amount)
            self.set_pixel_rgb(p, *color_rgb)
