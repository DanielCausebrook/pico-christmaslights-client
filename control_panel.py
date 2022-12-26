from __future__ import annotations

import colorsys
import copy
from typing import List, Union, Optional

import pygame
import pygame.freetype
from pygame.rect import Rect
from pygame.surface import Surface, SurfaceType

import colors
from pattern import LightPattern
from mathfun import *
from palette import Palette
from patterns.solid_color import SolidColorPattern
from transition import TransitionFactory
from transitions.fade import FadeTransitionFactory

pygame.init()
display_width = 720
display_height = 360
display_padding = 20
leds_y = display_padding + 5
big_buttons_x = display_padding + 10
big_buttons_y = display_padding + 60
big_button_w = 150
big_button_h = 25
big_button_spacing_x = 15
big_button_spacing_y = 5
big_button_color = pygame.Color(*rgb_to_bytes(colorsys.hsv_to_rgb(0, 0, 0.25)))
big_button_color_selected = pygame.Color(*rgb_to_bytes(colorsys.hsv_to_rgb(0.66, 0.8, 0.5)))
GAME_FONT = pygame.freetype.Font("resources/RobotoSlab-VariableFont_wght.ttf", 14)

PATTERN_TRANSITION_TIME_S = 2
PALETTE_TRANSITION_TIME_S = 2


class ControlPanel(LightPattern):
    screen: Union[Surface, SurfaceType]

    patterns: List[LightPattern] = []
    pattern_name_overrides: List[Optional[str]] = []
    current_pattern: Optional[LightPattern] = None

    transitions: List[TransitionFactory] = []
    transition_name_overrides: List[Optional[str]] = []
    current_transition: Optional[TransitionFactory] = None

    palettes: List[Palette] = []
    palette_names: List[str] = []
    current_palette: Palette = None
    selected_palette: Optional[Palette] = None
    palette_transition_amount = 1

    running: bool

    def __init__(self, num_pixels: int):
        super().__init__(num_pixels)

        pygame.display.set_icon(pygame.image.load("resources/light_controller_icon.png"))
        pygame.display.set_caption("Christmas Lights Control Panel")
        self.screen = pygame.display.set_mode((display_width, display_height))
        self.screen.fill(pygame.Color((0, 0, 0)))

        off = SolidColorPattern(num_pixels, colors.BLACK)
        self.add_pattern(off, "Lights Off")
        self.current_pattern = off

        fade = FadeTransitionFactory()
        self.add_transition(fade)
        self.current_transition = fade

        self.current_palette = Palette(colors.BLACK, colors.BLACK, colors.BLACK)

        self.running = True

        self.__draw_buttons()
        pygame.display.update()

    def is_running(self) -> bool:
        return self.running

    def add_pattern(self, pattern: LightPattern, name: Optional[str] = None) -> ControlPanel:
        self.patterns.append(pattern)
        self.pattern_name_overrides.append(name)
        return self

    def set_pattern(self, pattern: LightPattern) -> ControlPanel:
        if self.current_transition is None:
            self.current_pattern = pattern
        else:
            self.current_pattern = self.current_transition.new_transition(
                self.num_pixels,
                self.current_pattern,
                pattern,
                PATTERN_TRANSITION_TIME_S
            )
        return self

    def add_transition(self, transition: TransitionFactory, name: Optional[str] = None) -> ControlPanel:
        self.transitions.append(transition)
        self.transition_name_overrides.append(name)
        return self

    def set_transition(self, transition: TransitionFactory) -> ControlPanel:
        self.current_transition = transition
        return self

    def add_palette(self, palette: Palette, name: str) -> ControlPanel:
        self.palettes.append(palette)
        self.palette_names.append(name)
        return self

    def set_palette(self, palette: Palette) -> ControlPanel:
        self.current_palette = copy.copy(palette)
        return self

    def __get_big_button_rect(self, row: int, col: int) -> Rect:
        return pygame.Rect(
            big_buttons_x + row * (big_button_w + big_button_spacing_x),
            big_buttons_y + col * (big_button_h + big_button_spacing_y),
            big_button_w,
            big_button_h
        )

    def __draw_buttons(self) -> None:
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (big_buttons_x, big_buttons_y - 20, (big_button_w + big_button_spacing_x) * 3 - big_button_spacing_x, 20)
        )

        text_surface, rect = GAME_FONT.render('Patterns', (180, 180, 180), style=pygame.freetype.STYLE_STRONG)
        self.screen.blit(text_surface, (big_buttons_x + 44, big_buttons_y - 19))

        text_surface, rect = GAME_FONT.render('Transitions', (180, 180, 180), style=pygame.freetype.STYLE_STRONG)
        self.screen.blit(text_surface, (big_buttons_x + big_button_w + big_button_spacing_x + 34, big_buttons_y - 19))

        text_surface, rect = GAME_FONT.render('Palettes', (180, 180, 180), style=pygame.freetype.STYLE_STRONG)
        self.screen.blit(text_surface, (big_buttons_x + (big_button_w + big_button_spacing_x) * 2 + 44, big_buttons_y - 19))

        for i in range(len(self.patterns)):
            area = self.__get_big_button_rect(0, i)
            color = big_button_color_selected if self.current_pattern == self.patterns[i] else big_button_color
            pygame.draw.rect(self.screen, color, area)
            if self.pattern_name_overrides[i] is not None:
                name = self.pattern_name_overrides[i]
            else:
                name = self.patterns[i].get_name()
            text_surface, rect = GAME_FONT.render(name, (255, 255, 255))
            self.screen.blit(text_surface, (area.x + 4, area.y + 6), (0, 0, area.w - 8, area.h - 9))
        for i in range(len(self.transitions)):
            area = self.__get_big_button_rect(1, i)
            color = big_button_color_selected if self.current_transition == self.transitions[i] else big_button_color
            pygame.draw.rect(self.screen, color, area)
            if self.transition_name_overrides[i] is not None:
                name = self.transition_name_overrides[i]
            else:
                name = self.transitions[i].get_name()
            text_surface, rect = GAME_FONT.render(name, (255, 255, 255))
            self.screen.blit(text_surface, (area.x + 4, area.y + 6), (0, 0, area.w - 8, area.h - 9))
        for i in range(len(self.palettes)):
            area = self.__get_big_button_rect(2, i)
            color = big_button_color_selected if self.selected_palette == self.palettes[i] else big_button_color
            pygame.draw.rect(self.screen, color, area)
            text_surface, rect = GAME_FONT.render(self.palette_names[i], (255, 255, 255))
            self.screen.blit(text_surface, (area.x + 4, area.y + 6), (0, 0, area.w - 8, area.h - 9))

    def do_main_loop(self, t: float, delta_t: float, palette: Palette) -> None:

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                for i in range(len(self.patterns)):
                    button_rect = self.__get_big_button_rect(0, i)
                    if self.patterns[i] != self.current_pattern and button_rect.collidepoint(click_pos):
                        self.set_pattern(self.patterns[i])
                        break
                for i in range(len(self.transitions)):
                    button_rect = self.__get_big_button_rect(1, i)
                    if self.transitions[i] != self.current_transition and button_rect.collidepoint(click_pos):
                        self.set_transition(self.transitions[i])
                        break
                for i in range(len(self.palettes)):
                    button_rect = self.__get_big_button_rect(2, i)
                    if self.palettes[i] != self.selected_palette and button_rect.collidepoint(click_pos):
                        self.selected_palette = self.palettes[i]
                        self.palette_transition_amount = 0
                        break

        if self.palette_transition_amount < 1:
            self.palette_transition_amount += delta_t
            if self.palette_transition_amount > 1:
                self.current_palette = copy.copy(self.selected_palette)
            else:
                transition_time_left = (1 - self.palette_transition_amount) * PALETTE_TRANSITION_TIME_S
                interp_amount = min(1.0, delta_t / transition_time_left)

                self.current_palette = Palette(
                    self.current_palette.primary.interp(self.selected_palette.primary, interp_amount),
                    self.current_palette.secondary.interp(self.selected_palette.secondary, interp_amount),
                    self.current_palette.accent.interp(self.selected_palette.accent, interp_amount)
                )

        if self.current_pattern is not None:
            self.current_pattern = self.current_pattern.unwrap()
            self.pixels = self.current_pattern.main_loop(t, delta_t, self.current_palette)
        else:
            self.clear()

        self.__draw_buttons()

        for i in range(self.num_pixels):
            x = self.num_pixels - i - 1
            pygame.draw.circle(
                self.screen,
                pygame.Color(*self.pixels[i].get_bytes()).correct_gamma(0.5),
                (display_padding + x * ((display_width - 2 * display_padding) / self.num_pixels), leds_y),
                2
            )

        pygame.display.update()
