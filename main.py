import datetime
import time

import opensimplex

import colors
from colors import HSVColor, RGBColor, Color
from control_panel import ControlPanel
from palette import Palette
from pattern_layered import LayeredPattern
from patterns.bouncing_blocks import BouncingBlocksPattern
from patterns.bubble_sort import BubbleSortPattern
from patterns.simple_stripes import SimpleStripesPattern
from patterns.gentle_2tone import Gentle2TonePattern
from patterns.gentle_with_rainbows import GentleWithRainbowsPattern
from patterns.sparkle_comets import SparkleCometPattern
from patterns.sparkles import Sparkles
from patterns.warp_drive import WarpDrivePattern
from pico_client import *
from mathfun import smoothstep
from transitions.wipe import WipeTransitionFactory

PREVIEW_ONLY = False
BRIGHTNESS = 1

num_pixels = 200
lights = PicoNeopixel("192.168.1.135", num_pixels) if not PREVIEW_ONLY else None

C_BLACK = RGBColor(0, 0, 0)
C_WHITE = RGBColor(1, 1, 1)
C_RED = HSVColor(0, 1, 1)
C_GOLD = HSVColor(15 / 255, 1, 1)
C_ORANGE = HSVColor(0.04, 1, 1)
C_YELLOW = HSVColor(0.08, 1, 1)
C_GREEN = HSVColor(0.33, 1, 1)
C_TEAL = HSVColor(0.37, 1, 1)
C_TURQUOISE = HSVColor(0.45, 1, 1)
C_BLUE_LIGHT = HSVColor(0.55, 1, 1)
C_BLUE = HSVColor(0.65, 1, 1)
C_BLUE_PURPLE = HSVColor(0.7, 1, 1)
C_PURPLE = HSVColor(0.75, 1, 1)
C_PURPLE_PINKY = HSVColor(0.85, 1, 1)
C_PINK = HSVColor(0.95, 1, 1)


test_color = C_TEAL
test_color2 = C_GREEN
# test_color3 = C_GREEN
test_palette = Palette(test_color, test_color, C_WHITE)
test_palette2 = Palette(test_color2, test_color2, C_WHITE)
# test_palette3 = Palette(test_color3, test_color3)
blue_purple_palette = Palette(C_BLUE, C_PURPLE_PINKY, colors.WHITE)
blue_white_palette = Palette(C_BLUE, HSVColor(0.55, 0.6, 1), C_WHITE)
christmas_palette = Palette(C_RED, C_GREEN, C_WHITE)
gold_palette = Palette(C_GOLD, C_WHITE, C_RED)
gold_red_palette = Palette(C_GOLD, C_RED, C_WHITE)
red_gold_palette = Palette(C_RED, C_GOLD, C_WHITE)
red_teal_palette = Palette(C_RED, C_TEAL, C_WHITE)
DEFAULT_PALETTE = red_teal_palette

smooth_wipe_transition = WipeTransitionFactory(softness=80, reverse=True)
opensimplex.random_seed()

gentle_with_rainbows_and_sparkles = LayeredPattern(num_pixels)
gentle_with_rainbows_and_sparkles.add_layer(GentleWithRainbowsPattern(num_pixels))
gentle_with_rainbows_and_sparkles.add_layer(Sparkles(num_pixels, 0.8, 3))

control_panel = ControlPanel(num_pixels)\
    .add_pattern(BouncingBlocksPattern(num_pixels))\
    .add_pattern(GentleWithRainbowsPattern(num_pixels))\
    .add_pattern(Gentle2TonePattern(num_pixels))\
    .add_pattern(SimpleStripesPattern(num_pixels, width=7, speed=14))\
    .add_pattern(WarpDrivePattern(num_pixels))\
    .add_pattern(Sparkles(num_pixels, 1, 3))\
    .add_pattern(SparkleCometPattern(num_pixels))\
    .add_pattern(BubbleSortPattern(num_pixels))\
    .add_pattern(gentle_with_rainbows_and_sparkles, name='Rainbows & Sparkles')\
    .add_transition(smooth_wipe_transition, name='Wipe smooth')\
    .add_transition(WipeTransitionFactory(softness=1, reverse=True), name='Wipe sharp')\
    .add_palette(gold_palette, 'Gold & White') \
    .add_palette(red_gold_palette, 'Royal')\
    .add_palette(christmas_palette, 'Candy Cane')\
    .add_palette(red_teal_palette, 'Red & Teal')\
    .add_palette(blue_purple_palette, 'Blue & Purple') \
    .add_palette(blue_white_palette, 'Ice') \
    .add_palette(Palette(C_BLUE, C_PURPLE, C_WHITE), 'Blue & Purple2')\
    .set_transition(smooth_wipe_transition)\
    .set_palette(DEFAULT_PALETTE)

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
    night_adjustment = smoothstep(8/24, 8.5/24, day_proportion) - smoothstep(22.5/23, 1, day_proportion)
    # night_adjustment = smoothstep(15.5/24, 16/24, day_proportion) - smoothstep(22.5/23, 1, day_proportion)
    # night_adjustment = 1
    night_brightness = 0.04 + 0.96 * night_adjustment
    night_time_dilation = 0.5 + 0.5 * night_adjustment

    t = time.time()
    delta_t = t - last_time

    start_time += delta_t * (1 - night_time_dilation)
    delta_t *= night_time_dilation

    frame = control_panel.main_loop(t - start_time, delta_t, DEFAULT_PALETTE)
    last_time = t

    frame = [frame[i].dim(BRIGHTNESS * night_brightness) for i in range(num_pixels)]

    if not PREVIEW_ONLY:
        lights.pixels = [color.get_bytes() for color in frame]
        lights.show()

    time.sleep(control_panel.get_delay_s())

if not PREVIEW_ONLY:
    lights.disconnect()
