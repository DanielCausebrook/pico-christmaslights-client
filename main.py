import time

import opensimplex

from control_panel import ControlPanel
from palette import Palette
from patterns.bouncing_blocks import BouncingBlocksPattern
from patterns.gentle_2tone import Gentle2TonePattern
from patterns.gentle_with_rainbows import GentleWithRainbowsPattern
from blended_pattern import BlendedPattern
from patterns.off import OffPattern
from pico_client import *
from mathfun import rgb_to_bytes

num_pixels = 200
lights = PicoNeopixel("192.168.1.135", num_pixels)
palette = Palette()
opensimplex.random_seed()


def get_patterns():
    off_pattern = OffPattern(num_pixels)
    bouncing_blocks_pattern = BouncingBlocksPattern(num_pixels)
    gentle_with_rainbows_pattern = GentleWithRainbowsPattern(num_pixels)
    # hybrid_test = HybridPattern(num_pixels, [bouncing_blocks_pattern, gentle_with_rainbows_pattern])
    # # for p in range(num_pixels):
    # #     p_prop = p/num_pixels
    # #     hybrid_test.set_pixel_mix(p, [p_prop, 1-p_prop])
    # hybrid_test.set_mix([0.5, 0.5])

    return [
        off_pattern,
        bouncing_blocks_pattern,
        gentle_with_rainbows_pattern,
        # hybrid_test,
        Gentle2TonePattern(num_pixels),
    ], off_pattern


control_panel = ControlPanel(num_pixels, *get_patterns())

BRIGHTNESS = 1

start_time = time.time()
last_time = start_time

while control_panel.is_running():
    t = time.time()
    control_panel.main_loop(t - start_time, t - last_time, palette)
    last_time = t

    frame = control_panel.get_frame()

    for x in range(num_pixels):
        frame[x] = (
            frame[x][0] * BRIGHTNESS,
            frame[x][1] * BRIGHTNESS,
            frame[x][2] * BRIGHTNESS
        )

    lights.pixels = [rgb_to_bytes(x) for x in frame]
    lights.show()

    time.sleep(control_panel.get_delay_s())
