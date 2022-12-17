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
        primary_hsv = colorsys.rgb_to_hsv(*palette.primary)
        secondary_hsv = colorsys.rgb_to_hsv(*palette.secondary)

        for x in range(self.num_pixels):
            noise = opensimplex.noise2(t + self.seed_bg, (x / 40) - (t / -4))
            color_hsv = hsv_interp(primary_hsv, secondary_hsv, smoothstep(-0.2, 0.2, noise))

            noise = opensimplex.noise2((t + self.seed_rainbow) / 2, (x / 80) - (t / 4))
            brighten = smoothstep(-0.35, -0.25, noise) - smoothstep(0.25, 0.35, noise)
            color_hsv = (
                (color_hsv[0] + smoothstep(-0.3, 0.3, noise)) % 1,
                color_hsv[1] + (1 - color_hsv[1]) * brighten,
                color_hsv[2] + (1 - color_hsv[2]) * brighten
            )

            self.set_pixel_hsv(x, *color_hsv)
