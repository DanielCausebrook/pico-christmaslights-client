from LightPattern import LightPattern
from patterns.gentle_2tone import Gentle2TonePattern
from pico_client import *
from mathfun import *
import opensimplex


class GentleWithRainbowsPattern(LightPattern):

    def __init__(self, num_pixels, seed_rainbow=0, seed_bg=0):
        super().__init__(num_pixels)
        self.seed_rainbow = seed_rainbow
        self.seed_bg = seed_bg

    def get_name(self):
        return 'Gentle with rainbows'

    def do_main_loop(self, t, delta_t, palette):
        for x in range(self.num_pixels):
            noise = opensimplex.noise2(t + self.seed_bg, (x / 40) - (t / -4))
            color_rgb = rgb_interp(palette.primary, palette.secondary, smoothstep(-0.2, 0.2, noise))
            color_hsv = colorsys.rgb_to_hsv(*color_rgb)

            noise = opensimplex.noise2((t + self.seed_rainbow) / 2, (x / 80) - (t / 4))
            color_hsv = (
                (color_hsv[0] + smoothstep(-0.3, 0.3, noise)) % 1,
                color_hsv[1],
                color_hsv[2]
            )

            self.set_pixel_hsv(x, *color_hsv)
