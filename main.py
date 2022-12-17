import time

import opensimplex
import pygame
import pygame.freetype

from patterns.bouncing_blocks import BouncingBlocksPattern
from patterns.gentle_blue_with_rainbows import GentleBlueWithRainbowsPattern
from hybrid_pattern import HybridPattern
from pico_client import *
from mathfun import rgb_to_bytes

num_pixels = 200

bouncing_blocks_pattern = BouncingBlocksPattern(num_pixels)
gentle_pattern = GentleBlueWithRainbowsPattern(num_pixels)
hybrid_test = HybridPattern(num_pixels, [bouncing_blocks_pattern, gentle_pattern])
# for p in range(num_pixels):
#     p_prop = p/num_pixels
#     hybrid_test.set_pixel_mix(p, [p_prop, 1-p_prop])
hybrid_test.set_mix([0.5, 0.5])

patterns = [
    bouncing_blocks_pattern,
    gentle_pattern,
    hybrid_test
]
curr_pattern_index = 2

brightness_modifier = 1

lights = PicoNeopixel("192.168.1.135", num_pixels)

opensimplex.random_seed()

pygame.init()
display_width = 720
display_height = 360
display_padding = 20
display_leds_y = display_padding + 0
display_patterns_x = display_padding + 20
display_patterns_y = display_padding + 40
display_patterns_w = 150
display_patterns_button_h = 25
display_patterns_button_color = pygame.Color(*rgb_to_bytes(colorsys.hsv_to_rgb(0, 0, 0.6)))
display_patterns_button_color_selected = pygame.Color(*rgb_to_bytes(colorsys.hsv_to_rgb(0.66, 0.8, 0.6)))
GAME_FONT = pygame.freetype.Font("resources/RobotoSlab-VariableFont_wght.ttf", 14)
screen = pygame.display.set_mode((display_width, display_height))
screen.fill(pygame.Color((0, 0, 0)))


def get_pattern_button_rect(pattern):
    return pygame.Rect(
                display_patterns_x,
                display_patterns_y + pattern * (display_patterns_button_h + 5),
                display_patterns_w,
                display_patterns_button_h
            )


def check_pattern_button_clicked(mousePos):
    for p in range(len(patterns)):
        if get_pattern_button_rect(p).collidepoint(mousePos):
            return p
    return None


def draw_pattern_buttons():
    for p in range(len(patterns)):
        area = get_pattern_button_rect(p)
        color = display_patterns_button_color_selected if curr_pattern_index == p else display_patterns_button_color
        pygame.draw.rect(screen, color, area)
        text_surface, rect = GAME_FONT.render(patterns[p].get_name(), (255, 255, 255))
        screen.blit(text_surface, (area.x + 4, area.y + 6), (0, 0, area.w - 8, area.h - 12))


draw_pattern_buttons()

pygame.display.update()

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            pattern = check_pattern_button_clicked(pygame.mouse.get_pos())
            if pattern is not None:
                curr_pattern_index = pattern
                draw_pattern_buttons()

    t = time.time()
    patterns[curr_pattern_index].main_loop(t - start_time)

    frame = patterns[curr_pattern_index].get_frame()

    for x in range(num_pixels):
        frame[x] = (
            frame[x][0] * brightness_modifier,
            frame[x][1] * brightness_modifier,
            frame[x][2] * brightness_modifier
        )
        pygame.draw.circle(
            screen,
            pygame.Color(*rgb_to_bytes(frame[x])).correct_gamma(0.5),
            (display_padding + x * ((display_width - 2*display_padding) / num_pixels), display_padding),
            1.5
        )
    pygame.display.update()

    lights.pixels = [rgb_to_bytes(x) for x in frame]
    lights.show()

    time.sleep(patterns[curr_pattern_index].get_delay_s())
