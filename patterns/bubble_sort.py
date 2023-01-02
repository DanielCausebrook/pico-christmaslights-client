import math
import random
from typing import List

from colors import HSVColor
from effects.hue_rotate import HueRotateEffect
from palette import Palette
from pattern import LightPattern
from transitions.fade import FadeTransition

steps_per_s = 100

class BubbleSortPattern(LightPattern):
    start_in_s: float
    values: List[float]
    bubble_sort_location: int
    num_sorted: int
    ended: bool
    reverse: bool

    def __init__(self, num_pixels: int, delay_start_s: float = 2):
        super().__init__(num_pixels)
        self.values = [i/num_pixels for i in range(num_pixels)]
        random.shuffle(self.values)
        self.bubble_sort_location = 0
        self.num_sorted = 0
        self.start_in_s = delay_start_s
        self.ended = False
        self.reverse = False
        self.add_effect(HueRotateEffect())

    def get_name(self):
        return 'Bubble Sort'

    def unwrap(self) -> LightPattern:
        if self.num_sorted >= self.num_pixels - 1 and not self.ended:
            self.ended = True
            return FadeTransition(self.num_pixels, self, BubbleSortPattern(self.num_pixels, 2), 2)
        else:
            return self

    def do_main_loop(self, t: float, delta_t: float, palette: Palette) -> None:
        num_steps = math.floor(delta_t * steps_per_s)

        for _ in range(num_steps):
            if self.reverse:
                loc = self.num_pixels - self.bubble_sort_location - 2
            else:
                loc = self.bubble_sort_location
            if self.values[loc] > self.values[loc + 1]:
                temp = self.values[loc]
                self.values[loc] = self.values[loc + 1]
                self.values[loc + 1] = temp
            self.bubble_sort_location += 1
            if self.bubble_sort_location >= self.num_pixels - math.floor(self.num_sorted / 2) - 1:
                self.num_sorted += 1
                self.bubble_sort_location = math.floor(self.num_sorted / 2)
                self.reverse = not self.reverse

        for i in range(self.num_pixels):
            self.set_pixel(i, HSVColor(self.values[i], 1, 1))