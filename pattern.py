from __future__ import annotations

import copy
from typing import Optional, List

import colors
from colors import Color
from effect import Effect
from palette import Palette


def rgb_to_bytes(rgb):
    (r, g, b) = rgb
    return round(r * 255), round(g * 255), round(b * 255)


class LightPattern:
    num_pixels: int
    pixels: List[Color]
    effects: List[Effect]
    palette_override: Optional[Palette]
    last_t: Optional[float]

    def __init__(self, num_pixels: int):
        self.num_pixels = num_pixels
        self.pixels = [colors.BLACK for _ in range(num_pixels)]
        self.effects = []
        self.palette_override = None
        self.last_t = None

    def get_name(self):
        return type(self).__name__

    def override_palette(self, palette: Optional[Palette]) -> LightPattern:
        self.palette_override = palette
        return self

    def add_effect(self, effect: Effect):
        self.effects.append(effect)

    def unwrap(self) -> LightPattern:
        """
        Returns a new LightPattern (if any) to use in place of this one.

        For LightPatterns which wrap other patterns, such as transitions, we need a method to dispose of the transition
        layer once it is done. Any class which contains other LightPatterns may periodically call
        `pattern = pattern.unwrap()` to remove any redundant or completed patterns.
        :return:
        """
        return self

    def clear(self):
        """
        Sets all pixel values to off/black (0, 0, 0).

        Remember to call show() to send all pixel values to the lights.
        """
        self.pixels = [colors.BLACK.set_alpha(0) for _ in range(self.num_pixels)]

    def set_pixel(self, pixel: int, color: Color):
        """
        Sets the colour of a pixel.

        Remember to call show() to send all pixel values to the lights.
        :param int pixel: Pixel index
        :param Color color: The color to set
        """
        self.pixels[pixel] = color

    def main_loop(self, t: float, delta_t: float, palette: Palette) -> List[Color]:
        """
        :param float delta_t:
        :param Palette palette:
        :param float t:
        """
        if self.last_t == t:
            pass
        else:
            self.do_main_loop(t, delta_t, palette if self.palette_override is None else self.palette_override)
            for effect in self.effects:
                self.pixels = effect.apply_main_loop(self.pixels, t, delta_t)
            self.last_t = t

        return copy.copy(self.pixels)

    def do_main_loop(self, t: float, delta_t: float, palette: Palette) -> None:
        """
        :param Palette palette:
        :param float t:
        :param float delta_t:
        """
        raise "do_main_loop() must be overridden in subclass."


    def get_delay_s(self) -> float:
        return 0.02



