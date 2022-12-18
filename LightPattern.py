from __future__ import annotations

import colorsys
from typing import Optional, List, Tuple

from palette import Palette


def rgb_to_bytes(rgb):
    (r, g, b) = rgb
    return round(r * 255), round(g * 255), round(b * 255)


class LightPattern:
    num_pixels: int
    palette_override: Optional[Palette] = None

    def __init__(self, num_pixels):
        self.num_pixels = num_pixels
        self.last_t = None
        self.pixels = []
        for p in range(num_pixels):
            self.pixels.append((0.0, 0.0, 0.0))

    def get_name(self):
        return type(self).__name__

    def override_palette(self, palette: Optional[Palette]):
        self.palette_override = palette

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
        for p in range(self.num_pixels):
            self.pixels[p] = (0, 0, 0)

    def set_pixel_hsv(self, pixel, h, s, v):
        """
        Sets the colour of a pixel to a HSV value.

        Remember to call show() to send all pixel values to the lights.
        :param int pixel: Pixel index
        :param float h: Hue, in range [0, 1]
        :param float s: Saturation, in range [0, 1]
        :param float v: Value, in range [0, 1]
        """
        if pixel > self.num_pixels - 1:
            raise "Provided pixel index (" + str(pixel) + ") is too large (numPixels: " + str(self.num_pixels) + ")."
        if h < 0 or h > 1:
            raise "Hue must be in range [0, 1]"
        if s < 0 or s > 1:
            raise "Saturation must be in range [0, 1]"
        if v < 0 or v > 1:
            raise "Value must be in range [0, 1]"
        self.pixels[pixel] = colorsys.hsv_to_rgb(h, s, v)

    def set_pixel_rgb(self, pixel, r, g, b):
        """
        Sets the colour of a pixel to an RGB value.

        Remember to call show() to send all pixel values to the lights.
        :param int pixel: Pixel index
        :param float r: Red component, in range [0,1]
        :param float g: Green component, in range [0,1]
        :param float b: Blue component, in range [0,1]
        """
        if r < 0 or r > 1:
            raise "Red must be in range [0, 1]"
        if g < 0 or g > 1:
            raise "Green must be in range [0, 1]"
        if b < 0 or b > 1:
            raise "Blue must be in range [0, 1]"
        self.pixels[pixel] = (r, g, b)

    def main_loop(self, t: float, delta_t: float, palette: Palette) -> List[Tuple[float, float, float]]:
        """
        :param float delta_t:
        :param Palette palette:
        :param float t:
        """
        if self.last_t is None:
            self.do_main_loop(t, delta_t, palette if self.palette_override is None else self.palette_override)
            self.last_t = t
        elif self.last_t == t:
            pass
        else:
            self.do_main_loop(t, delta_t, palette if self.palette_override is None else self.palette_override)
            self.last_t = t

        return self.pixels

    def do_main_loop(self, t: float, delta_t: float, palette: Palette):
        """
        :param Palette palette:
        :param float t:
        :param float delta_t:
        """
        raise "do_main_loop() must be overridden in subclass."


    def get_delay_s(self):
        return 0.02

    def get_frame(self):
        return self.pixels

