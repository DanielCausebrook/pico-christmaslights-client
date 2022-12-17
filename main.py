import math
import time

import pygame

from bouncing_blocks import BouncingBlocksPattern
from gentle_blue_with_rainbows import GentleBlueWithRainbowsPattern
from pico_client import *

num_pixels = 200
patterns = [
    BouncingBlocksPattern(num_pixels),
    GentleBlueWithRainbowsPattern(num_pixels)
]
PATTERN = 1

brightness_modifier = 1

lights = PicoNeopixel("192.168.1.135", num_pixels)

pygame.init()
display_width = 480
display_height = 360
display_padding = 20
screen = pygame.display.set_mode((480, 360))

start_time = time.time()
last_time = start_time

running = True
while running:
    pixels = []

    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False

    t = time.time()
    patterns[PATTERN].main_loop(t - start_time, t - last_time)
    last_time = t

    lights.pixels = patterns[PATTERN].get_frame()

    for x in range(num_pixels):
        lights.pixels[x] = (
            math.floor(lights.pixels[x][0] * brightness_modifier),
            math.floor(lights.pixels[x][1] * brightness_modifier),
            math.floor(lights.pixels[x][2] * brightness_modifier)
        )

    lights.show()

    time.sleep(patterns[PATTERN].get_delay_s())
