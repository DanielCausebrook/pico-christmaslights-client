import colorsys
from typing import List, Union

import pygame
import pygame.freetype
from pygame.rect import Rect
from pygame.surface import Surface, SurfaceType

from LightPattern import LightPattern
from palette import Palette
from mathfun import *

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
    selected_pattern_index: int
    running: bool

    def __init__(self, num_pixels: int, patterns: List[LightPattern], selected_pattern_index=0):
        super().__init__(num_pixels)

        self.screen = pygame.display.set_mode((display_width, display_height))
        self.screen.fill(pygame.Color((0, 0, 0)))
        self.patterns = patterns
        self.selected_pattern_index = selected_pattern_index
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

    def __draw_pattern_buttons(self):
        for p in range(len(self.patterns)):
            area = self.__get_pattern_button_rect(p)
            color = display_patterns_button_color_selected if self.selected_pattern_index == p else display_patterns_button_color
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
                pattern_button_clicked = None
                for p in range(len(self.patterns)):
                    if self.__get_pattern_button_rect(p).collidepoint(pygame.mouse.get_pos()):
                        pattern_button_clicked = p
                        break
                if pattern_button_clicked is not None:
                    self.selected_pattern_index = pattern_button_clicked
                    self.__draw_pattern_buttons()

        self.patterns[self.selected_pattern_index].main_loop(t, delta_t, palette)

        frame = self.patterns[self.selected_pattern_index].get_frame()

        for p in range(self.num_pixels):
            pygame.draw.circle(
                self.screen,
                pygame.Color(*rgb_to_bytes(frame[p])).correct_gamma(0.5),
                (display_padding + p * ((display_width - 2*display_padding) / self.num_pixels), display_padding),
                2
            )

        self.pixels = frame

        pygame.display.update()
