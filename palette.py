from dataclasses import dataclass

from colors import Color


@dataclass(frozen=True)
class Palette:
    primary: Color
    secondary: Color
    accent: Color