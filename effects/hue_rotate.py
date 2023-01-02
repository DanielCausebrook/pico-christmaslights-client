from typing import List

from colors import Color, HSVColor
from effect import Effect


class HueRotateEffect(Effect):
    shift: float = 0

    def apply_main_loop(self, frame: List[Color], t: float, delta_t: float) -> List[Color]:
        result = []
        for i in range(len(frame)):
            color = frame[i].get_hsv()
            result.append(HSVColor((color.h + self.shift) % 1, color.s, color.v))
        self.shift += delta_t / 8
        return result
