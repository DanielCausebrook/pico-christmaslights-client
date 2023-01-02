import random
from typing import List

from colors import Color, RGBColor
from effect import Effect
from effects.persistence import PersistenceEffect
from palette import Palette
from pattern import LightPattern


class Sparkles(LightPattern):
    def __init__(self, num_pixels: int, amount: float, decay_rate: float):
        super().__init__(num_pixels)
        self.amount: float = amount
        self.add_effect(PersistenceEffect(num_pixels, decay_rate))

    def get_name(self):
        return "Sparkles"

    def do_main_loop(self, t: float, delta_t: float, palette: Palette) -> None:
        self.clear()
        for i in range(self.num_pixels):
            if random.uniform(0, 1) < self.amount * delta_t:
                self.set_pixel(i, palette.accent)
