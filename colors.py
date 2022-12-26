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
    def add_alpha(self, alpha: float = 1) -> AlphaColor:
        pass

    @abstractmethod
    def dim(self, brightness: float) -> Color:
        pass

    @abstractmethod
    def interp(self, other: Color, amount: float) -> Color:
        pass

    def screen_with(self, color: AlphaColor) -> Color:
        return self.interp(color, color.get_alpha())

    def get_bytes(self) -> Tuple[int, int, int]:
        rgb = self.get_rgb()
        return round(rgb.r * 255), round(rgb.g * 255), round(rgb.b * 255)


@dataclass(frozen=True)
class AlphaColor(Color, ABC):

    @abstractmethod
    def get_alpha(self) -> float:
        pass

    @abstractmethod
    def get_rgba(self) -> RGBAColor:
        pass

    @abstractmethod
    def get_hsva(self) -> HSVAColor:
        pass

    @abstractmethod
    def drop_alpha(self) -> Color:
        pass

    def screen_with(self, color: AlphaColor) -> AlphaColor:
        raise "I don't know how to screen a ColorA with a ColorA yet, sorry!"


@dataclass(frozen=True)
class RGBColor(Color):
    r: float
    g: float
    b: float

    def get_rgb(self) -> RGBColor:
        return self

    def get_hsv(self) -> HSVColor:
        return HSVColor(*colorsys.rgb_to_hsv(self.r, self.g, self.b))

    def add_alpha(self, alpha: float = 1) -> RGBAColor:
        return RGBAColor(self.r, self.g, self.b, alpha)

    def dim(self, brightness: float) -> RGBColor:
        return BLACK.interp(self, brightness)

    def interp(self, other: Color, amount: float) -> RGBColor:
        other = other.get_rgb()
        return RGBColor(*rgb_interp((self.r, self.g, self.b), (other.r, other.g, other.b), amount))

@dataclass(frozen=True)
class RGBAColor(RGBColor, AlphaColor):
    r: float
    g: float
    b: float
    a: float

    def get_alpha(self) -> float:
        return self.a

    def get_rgb(self) -> RGBColor:
        return RGBColor(*rgb_interp((0, 0, 0), (self.r, self.g, self.b), self.a))

    def get_hsv(self) -> HSVColor:
        return self.get_rgb().get_hsv()

    def get_rgba(self) -> RGBAColor:
        return self

    def get_hsva(self) -> HSVAColor:
        return HSVAColor(*colorsys.rgb_to_hsv(self.r, self.g, self.b), self.a)

    def drop_alpha(self) -> Color:
        return RGBColor(self.r, self.g, self.b)

@dataclass(frozen=True)
class HSVColor(Color):
    h: float
    s: float
    v: float

    def get_rgb(self) -> RGBColor:
        return RGBColor(*colorsys.hsv_to_rgb(self.h, self.s, self.v))

    def get_hsv(self) -> HSVColor:
        return self

    def add_alpha(self, alpha: float = 1) -> HSVAColor:
        return HSVAColor(self.h, self.s, self.v, alpha)

    def dim(self, brightness: float) -> HSVColor:
        return self.get_rgb().dim(brightness).get_hsv()

    def interp(self, other: Color, amount: float) -> HSVColor:
        return self.get_rgb().interp(other, amount).get_hsv()

@dataclass(frozen=True)
class HSVAColor(HSVColor, AlphaColor):
    h: float
    s: float
    v: float
    a: float

    def get_alpha(self) -> float:
        return self.a

    def get_rgb(self) -> RGBColor:
        return RGBColor(*rgb_interp((0, 0, 0), colorsys.hsv_to_rgb(self.h, self.s, self.v), self.a))

    def get_hsv(self) -> HSVColor:
        return self.get_rgb().get_hsv()

    def get_rgba(self) -> RGBAColor:
        return RGBAColor(*colorsys.hsv_to_rgb(self.h, self.s, self.v), self.a)

    def get_hsva(self) -> HSVAColor:
        return self

    def drop_alpha(self) -> Color:
        return HSVColor(self.h, self.s, self.v)

BLACK = RGBColor(0, 0, 0)
WHITE = RGBColor(1, 1, 1)