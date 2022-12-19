import datetime
import time

import opensimplex

from control_panel import ControlPanel
from palette import Palette
from patterns.bouncing_blocks import BouncingBlocksPattern
from patterns.simple_stripes import SimpleStripesPattern
from patterns.gentle_2tone import Gentle2TonePattern
from patterns.gentle_with_rainbows import GentleWithRainbowsPattern
from pico_client import *
from mathfun import rgb_to_bytes, smoothstep
from transitions.wipe import WipeTransitionFactory

num_pixels = 200
lights = PicoNeopixel("192.168.1.135", num_pixels)
palette = Palette()
christmas_palette = Palette(colorsys.hsv_to_rgb(0, 1, 1), colorsys.hsv_to_rgb(0.33, 1, 1))
opensimplex.random_seed()

control_panel = ControlPanel(num_pixels)\
    .add_pattern(BouncingBlocksPattern(num_pixels))\
    .add_pattern(GentleWithRainbowsPattern(num_pixels))\
    .add_pattern(Gentle2TonePattern(num_pixels))\
    .add_pattern(SimpleStripesPattern(num_pixels, width=10).override_palette(christmas_palette), name='Candy Stripes')\
    .add_transition(WipeTransitionFactory(softness=80), name='Wipe smooth')\
    .add_transition(WipeTransitionFactory(softness=1), name='Wipe sharp')

BRIGHTNESS = 1

start_time = time.time()
last_time = start_time

while control_panel.is_running():
    today = datetime.datetime.now()
    microseconds_today = (
            (
                    (
                            (today.hour * 60) + today.minute
                    ) * 60 + today.second
            ) * 1_000_000 + today.microsecond
    )
    day_proportion = microseconds_today / 86_400_000_000
    night_adjustment = smoothstep(8/24, 8.5/24, day_proportion) - smoothstep(23.5/24, 1, day_proportion)
    night_brightness = 0.04 + 0.96 * night_adjustment
    night_time_dilation = 0.5 + 0.5 * night_adjustment

    t = time.time()
    delta_t = t - last_time

    start_time += delta_t * (1 - night_time_dilation)
    delta_t *= night_time_dilation

    control_panel.main_loop(t - start_time, delta_t, palette)
    last_time = t

    frame = control_panel.get_frame()

    for x in range(num_pixels):
        frame[x] = (
            frame[x][0] * BRIGHTNESS * night_brightness,
            frame[x][1] * BRIGHTNESS * night_brightness,
            frame[x][2] * BRIGHTNESS * night_brightness
        )

    lights.pixels = [rgb_to_bytes(x) for x in frame]
    lights.pixels.reverse()
    lights.show()

    time.sleep(control_panel.get_delay_s())
