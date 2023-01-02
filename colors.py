from __future__ import annotations

import colorsys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple


def rgb_component_to_linear(x :float) -> float:
    if x >= 0.0031308:
        return 1.055 * x ** (1.0 / 2.4) - 0.055
    else:
        return 12.92 * x


def rgb_component_from_linear(x: float) -> float:
    if x >= 0.04045:
        return ((x + 0.055)/(1 + 0.055)) ** 2.4
    else:
        return x / 12.92


def rgb_interp(color1: Tuple[float, float, float], color2: Tuple[float, float, float], amount) -> Tuple[float, float, float]:
    r1 = rgb_component_to_linear(color1[0])
    r2 = rgb_component_to_linear(color2[0])
    r = r1 * (1-amount) + r2 * amount
    g1 = rgb_component_to_linear(color1[1])
    g2 = rgb_component_to_linear(color2[1])
    g = g1 * (1-amount) + g2 * amount
    b1 = rgb_component_to_linear(color1[2])
    b2 = rgb_component_to_linear(color2[2])
    b = b1 * (1-amount) + b2 * amount

    return rgb_component_from_linear(r), rgb_component_from_linear(g), rgb_component_from_linear(b)


@dataclass(frozen=True)
class Color(ABC):
    @abstractmethod
    def get_rgb(self) -> RGBColor:
        pass

    @abstractmethod
    def get_hsv(self) -> HSVColor:
        pass

    @abstractmethod
    def get_alpha(self) -> float:
        pass

    @abstractmethod
    def set_alpha(self, alpha: float) -> Color:
        pass

    @abstractmethod
    def dim(self, brightness: float) -> Color:
        pass

    @abstractmethod
    def interp(self, other: Color, amount: float) -> Color:
        pass

    def rover(self, color: Color) -> Color:
        color = color.get_rgb()
        c1 = color.get_rgb()
        r1 = rgb_component_to_linear(c1.r)
        g1 = rgb_component_to_linear(c1.g)
        b1 = rgb_component_to_linear(c1.b)
        c2 = self.get_rgb()
        r2 = rgb_component_to_linear(c2.r)
        g2 = rgb_component_to_linear(c2.g)
        b2 = rgb_component_to_linear(c2.b)
        aO = c1.a + c2.a * (1 - c1.a)

        if aO == 0:
            return BLACK.set_alpha(0)

        return RGBColor(
            rgb_component_from_linear((r1 * c1.a + r2 * c2.a * (1 - c1.a))/aO),
            rgb_component_from_linear((g1 * c1.a + g2 * c2.a * (1 - c1.a))/aO),
            rgb_component_from_linear((b1 * c1.a + b2 * c2.a * (1 - c1.a))/aO),
            aO
        )

    def get_bytes(self) -> Tuple[int, int, int]:
        rgb = BLACK.rover(self).get_rgb()
        return round(rgb.r * 255), round(rgb.g * 255), round(rgb.b * 255)


@dataclass(frozen=True)
class RGBColor(Color):
    r: float
    g: float
    b: float
    a: float = 1.0

    def get_rgb(self) -> RGBColor:
        return self

    def get_hsv(self) -> HSVColor:
        return HSVColor(*colorsys.rgb_to_hsv(self.r, self.g, self.b), self.a)

    def get_alpha(self) -> float:
        return self.a

    def set_alpha(self, alpha: float) -> RGBColor:
        return RGBColor(self.r, self.g, self.b, alpha)

    def dim(self, brightness: float) -> RGBColor:
        return BLACK.interp(self, brightness).set_alpha(self.a)

    def interp(self, other: Color, amount: float) -> RGBColor:
        if amount >= 1:
            return other.get_rgb()
        elif amount <= 0:
            return self
        other = other.get_rgb()
        alpha = (1 - amount) * self.a + amount * other.get_alpha()
        return RGBColor(*rgb_interp((self.r, self.g, self.b), (other.r, other.g, other.b), amount), alpha)

    def __str__(self):
        return "RGB(" + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + (", " + str(self.a) if self.a != 1 else "") + ")"

@dataclass(frozen=True)
class HSVColor(Color):
    h: float
    s: float
    v: float
    a: float = 1.0

    def get_rgb(self) -> RGBColor:
        return RGBColor(*colorsys.hsv_to_rgb(self.h, self.s, self.v), self.a)

    def get_hsv(self) -> HSVColor:
        return self

    def get_alpha(self) -> float:
        return self.a

    def set_alpha(self, alpha: float) -> HSVColor:
        return HSVColor(self.h, self.s, self.v, alpha)

    def dim(self, brightness: float) -> HSVColor:
        return self.get_rgb().dim(brightness).get_hsv()

    def interp(self, other: Color, amount: float) -> HSVColor:
        return self.get_rgb().interp(other, amount).get_hsv()

    def __str__(self):
        return "HSV(" + str(self.h) + ", " + str(self.s) + ", " + str(self.v) + (", " + str(self.a) if self.a != 1 else "") + ")"

BLACK = RGBColor(0, 0, 0)
WHITE = RGBColor(1, 1, 1)