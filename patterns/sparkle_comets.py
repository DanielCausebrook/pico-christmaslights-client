import math
import random
from typing import List

import colors
from colors import Color
from effects.persistence import PersistenceEffect
from palette import Palette
from pattern import LightPattern
from pattern_layered import LayeredPattern


class SparkleCometPattern(LayeredPattern):
    comet_positions: List[float]
    comet_vels: List[float]
    comet_color_types: List[int]
    comet_colors: List[Color]
    comet_next_sparkles_in_t: List[float]
    next_comet_l_in_t: float
    next_comet_r_in_t: float

    def __init__(self, num_pixels: int):
        super().__init__(num_pixels)

        self.comet_positions = []
        self.comet_vels = []
        self.comet_color_types = []
        self.comet_colors = []
        self.comet_next_sparkles_in_t = []
        self.next_comet_l_in_t = random.uniform(0, 3)
        self.next_comet_r_in_t = random.uniform(0, 3)

        class Comets(LightPattern):
            comet_decay = 1.3
            def __init__(self, parent: SparkleCometPattern):
                super().__init__(num_pixels)
                self.parent = parent
                self.add_effect(PersistenceEffect(num_pixels, self.comet_decay))
            def do_main_loop(self, t: float, delta_t: float, palette: Palette) -> None:
                self.clear()
                for i in range(len(self.parent.comet_positions)):
                    pos = self.parent.comet_positions[i]
                    vel = self.parent.comet_vels[i]
                    if vel > 0:
                        pixel_indexes = range(math.floor(pos), math.ceil(pos + vel * delta_t))
                    else:
                        pixel_indexes = range(math.floor(pos + vel * delta_t), math.ceil(pos))
                    for j in pixel_indexes:
                        if 0 <= j < self.num_pixels:
                            if self.parent.comet_color_types[i] == 0:
                                color = palette.primary
                            elif self.parent.comet_color_types[i] == 1:
                                color = palette.secondary
                            else:
                                color = self.parent.comet_colors[i]

                            self.set_pixel(j, color)

        self.add_layer(Comets(self))

        class Sparkles(LightPattern):
            sparkle_stddev = 4.0
            sparkle_decay = 4
            def __init__(self, parent: SparkleCometPattern):
                super().__init__(num_pixels)
                self.parent = parent
                self.add_effect(PersistenceEffect(num_pixels, self.sparkle_decay))
            def do_main_loop(self, t: float, delta_t: float, palette: Palette) -> None:
                self.clear()
                for i in range(len(self.parent.comet_positions)):
                    delta_t_left = delta_t
                    while self.parent.comet_next_sparkles_in_t[i] <= delta_t_left:
                        sparkle_pos = round(random.normalvariate(self.parent.comet_positions[i], self.sparkle_stddev))
                        if 0 <= sparkle_pos < self.num_pixels:
                            self.set_pixel(round(sparkle_pos), palette.accent)
                        delta_t_left -= self.parent.comet_next_sparkles_in_t[i]
                        self.parent.comet_next_sparkles_in_t[i] = random.uniform(0.01, 0.03)
                    self.parent.comet_next_sparkles_in_t[i] -= delta_t_left



        self.add_layer(Sparkles(self))

    def do_main_loop(self, t: float, delta_t: float, palette: Palette) -> None:
        super().do_main_loop(t, delta_t, palette)
        removed = 0
        for i in range(len(self.comet_positions)):
            i = i - removed
            pos = self.comet_positions[i]
            vel = self.comet_vels[i]
            pos += vel * delta_t
            if (vel > 0 and pos > self.num_pixels + 25) or (vel < 0 and pos < -25):
                self.comet_positions.pop(i)
                self.comet_vels.pop(i)
                self.comet_color_types.pop(i)
                self.comet_colors.pop(i)
                self.comet_next_sparkles_in_t.pop(i)
                removed += 1
            else:
                self.comet_positions[i] = pos

        def new_comet_color():
            type_random = random.uniform(0, 1)
            if type_random < 0.5:
                self.comet_color_types.append(0)
                self.comet_colors.append(colors.BLACK)
            elif type_random < 0.8:
                self.comet_color_types.append(1)
                self.comet_colors.append(colors.BLACK)
            else:
                self.comet_color_types.append(2)
                self.comet_colors.append(colors.HSVColor(random.uniform(0, 1), 1, 1))
            self.comet_next_sparkles_in_t.append(random.uniform(0.05, 0.5))

        if self.next_comet_l_in_t <= 0:
            self.comet_positions.append(-20)
            self.comet_vels.append(random.uniform(60, 90))
            new_comet_color()
            self.next_comet_l_in_t = random.uniform(0.5, 3)

        self.next_comet_l_in_t -= delta_t

        if self.next_comet_r_in_t <= 0:
            self.comet_positions.append(self.num_pixels + 20)
            self.comet_vels.append(random.uniform(-90, -60))
            new_comet_color()
            self.next_comet_r_in_t = random.uniform(0.5, 3)

        self.next_comet_r_in_t -= delta_t




