import colorsys
from typing import List, Union

import pygame
import pygame.freetype
from pygame.rect import Rect
from pygame.surface import Surface, SurfaceType

from LightPattern import LightPattern
from palette import Palette
from mathfun import *
from transition import Transition
from transitions.fade import FadeTransition
from transitions.wipe import WipeTransition

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


class ControlPanel(LightPattern):
    screen: Union[Surface, SurfaceType]
    patterns: List[LightPattern]
    current_pattern: LightPattern
    running: bool

    def __init__(self, num_pixels: int, patterns: List[LightPattern], current_pattern: LightPattern = None):
        super().__init__(num_pixels)

        pygame.display.set_caption("Christmas Lights Control Panel")
        self.screen = pygame.display.set_mode((display_width, display_height))
        self.screen.fill(pygame.Color((0, 0, 0)))
        self.patterns = patterns
        self.current_pattern = current_pattern
        self.running = True

        self.__draw_pattern_buttons()
        pygame.display.update()

    def is_running(self) -> bool:
        return self.running

    def add_pattern(self, pattern: LightPattern) -> None:
        self.patterns.append(pattern)

    def __get_pattern_button_rect(self, pattern_index) -> Rect:
        return pygame.Rect(
            display_patterns_x,
            display_patterns_y + pattern_index * (display_patterns_button_h + 5),
            display_patterns_w,
            display_patterns_button_h
        )

    def __draw_pattern_buttons(self) -> None:
        for p in range(len(self.patterns)):
            area = self.__get_pattern_button_rect(p)
            color = display_patterns_button_color_selected if self.current_pattern == self.patterns[
                p] else display_patterns_button_color
            pygame.draw.rect(self.screen, color, area)
            text_surface, rect = GAME_FONT.render(self.patterns[p].get_name(), (255, 255, 255))
            self.screen.blit(text_surface, (area.x + 4, area.y + 6), (0, 0, area.w - 8, area.h - 12))

    def do_main_loop(self, t: float, delta_t: float, palette: Palette) -> None:

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not isinstance(self.current_pattern, Transition):
                    for p in range(len(self.patterns)):
                        if self.patterns[p] != self.current_pattern and self.__get_pattern_button_rect(p).collidepoint(pygame.mouse.get_pos()):
                            self.current_pattern = WipeTransition(self.num_pixels, self.current_pattern, self.patterns[p], 2, 80)
                            break

        if self.current_pattern is not None:
            self.current_pattern = self.current_pattern.unwrap()
            self.pixels = self.current_pattern.main_loop(t, delta_t, palette)
        else:
            self.clear()

        self.__draw_pattern_buttons()

        for p in range(self.num_pixels):
            pygame.draw.circle(
                self.screen,
                pygame.Color(*rgb_to_bytes(self.pixels[p])).correct_gamma(0.5),
                (display_padding + p * ((display_width - 2 * display_padding) / self.num_pixels), display_padding),
                2
            )

        pygame.display.update()
