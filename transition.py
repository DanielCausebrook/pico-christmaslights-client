import copy
from typing import List

from colors import Color
from pattern import LightPattern
from palette import Palette


class TransitionFactory:
    def get_name(self):
        return type(self).__name__

    def new_transition(self, num_pixels: int, pattern1: LightPattern, pattern2: LightPattern, duration_s: float):
        raise "new_transition() must be implemented in child class."

class Transition(LightPattern):
    pattern1: LightPattern
    pattern2: LightPattern
    duration_s: float
    progress: float

    def __init__(self, num_pixels: int, pattern1: LightPattern, pattern2: LightPattern, duration_s: float):
        super().__init__(num_pixels)

        self.pattern1 = pattern1
        self.pattern2 = pattern2
        self.duration_s = duration_s
        self.progress = 0

    def get_progress(self) -> float:
        return self.progress

    def is_complete(self) -> bool:
        return self.progress >= 1

    def unwrap(self) -> LightPattern:
        if self.progress < 1:
            return self
        return self.pattern2

    def main_loop(self, t: float, delta_t: float, palette: Palette) -> List[Color]:
        """
        :param float delta_t:
        :param Palette palette:
        :param float t:
        """

        self.pattern1 = self.pattern1.unwrap()
        self.pattern2 = self.pattern2.unwrap()

        if self.last_t is None:
            self.do_main_loop(t, delta_t, palette)
            self.last_t = t
        elif self.last_t == t:
            pass
        else:
            self.progress += delta_t / self.duration_s

            if self.progress <= 0:
                self.pixels = self.pattern1.main_loop(t, delta_t, palette)
            elif self.progress >= 1:
                self.pixels = self.pattern2.main_loop(t, delta_t, palette)
            else:
                self.do_main_loop(t, delta_t, palette)
                self.last_t = t

        return copy.copy(self.pixels)
