from pico_client import *
from mathfun import *
import time
import opensimplex
import numpy as np

num_pixels = 200

lights = PicoNeopixel("10.0.1.34", num_pixels)
opensimplex.random_seed()

delay_s = 0.03
t = 0

while True:
    pixels = []

    for x in range(num_pixels):
        h = 0.6
        s = 1
        v = 1

        noise = opensimplex.noise2(t, (x / 40) - (t / -4))
        h += smoothstep(-0.2, 0.2, noise) / 4

        noise = opensimplex.noise2((t + 218987941) / 2, (x / 80) - (t / 4))
        h += smoothstep(-0.3, 0.3, noise)

        h = h % 1
        lights.set_hsv(x, h, s, v)
    lights.show()

    time.sleep(delay_s)
    t += delay_s
