from colors import HSVColor
from palette import Palette
from pattern import LightPattern
from mathfun import *
import opensimplex


class GentleWithRainbowsPattern(LightPattern):

    def __init__(self, num_pixels, seed_rainbow=0, seed_bg=0):
        super().__init__(num_pixels)
        self.seed_rainbow = seed_rainbow
        self.seed_bg = seed_bg

    def get_name(self):
        return 'Gentle with rainbows'

    def do_main_loop(self, t: float, delta_t: float, palette: Palette):
        for x in range(self.num_pixels):
            noise = opensimplex.noise2(t + self.seed_bg, (x / 40) - (t / -4))
            color = palette.primary.interp(palette.secondary, smoothstep(-0.2, 0.2, noise)).get_hsv()

            noise = opensimplex.noise2((t + self.seed_rainbow) / 2, (x / 80) - (t / 4))
            color = HSVColor(
                (color.h + smoothstep(-0.3, 0.3, noise)) % 1,
                color.s,
                color.v
            )

            self.set_pixel(x, color)
