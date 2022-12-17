import time

from LightPattern import LightPattern
from pico_client import *
from mathfun import *
import opensimplex


class GentleBlueWithRainbowsPattern(LightPattern):

    def __init__(self, num_pixels):
        super().__init__(num_pixels)

    def get_name(self):
        return 'Gentle with rainbows'

    def do_main_loop(self, t, delta_t):
        for x in range(self.num_pixels):
            h = 0.6
            s = 1
            v = 1

            noise = opensimplex.noise2(t, (x / 40) - (t / -4))
            h += smoothstep(-0.2, 0.2, noise) / 4

            noise = opensimplex.noise2((t + 218987941) / 2, (x / 80) - (t / 4))
            h += smoothstep(-0.3, 0.3, noise)

            h = h % 1
            self.set_pixel_hsv(x, h, s, v)


# num_pixels = 100
#
# lights = PicoNeopixel("192.168.1.135", num_pixels)
# opensimplex.random_seed()
#
# delay_s = 0.03
# t = 0
#
# while True:
#     for x in range(num_pixels):
#         h = 0.6
#         s = 1
#         v = 1
#
#         noise = opensimplex.noise2(t, (x / 40) - (t / -4))
#         h += smoothstep(-0.2, 0.2, noise) / 4
#
#         noise = opensimplex.noise2((t + 218987941) / 2, (x / 80) - (t / 4))
#         h += smoothstep(-0.3, 0.3, noise)
#
#         h = h % 1
#         lights.set_hsv(x, h, s, v)
#
#     lights.show()
#
#     time.sleep(delay_s)
#     t += delay_s
