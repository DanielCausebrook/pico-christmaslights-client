from LightPattern import LightPattern
from pico_client import *
from mathfun import *
import opensimplex


class Gentle2TonePattern(LightPattern):

    def __init__(self, num_pixels, speed=1, gradient_width=0.2, seed=0):
        super().__init__(num_pixels)
        self.seed = seed
        self.speed = speed
        self.gradient_width = gradient_width

    def get_name(self):
        return 'Gentle 2Tone'

    def do_main_loop(self, t, delta_t, palette):
        for x in range(self.num_pixels):
            noise = opensimplex.noise2((t + self.seed) * self.speed, (x / 40) - (t / -4))
            color_hsv = rgb_interp(
                palette.primary,
                palette.secondary,
                smoothstep(-self.gradient_width, self.gradient_width, noise)
            )

            self.set_pixel_rgb(x, *color_hsv)
