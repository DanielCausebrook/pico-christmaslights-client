import dataclasses
import math
import random
from typing import List

import colors
from colors import HSVColor, HSVAColor
from pattern import LightPattern
from mathfun import smoothstep
from palette import Palette


class WarpDrivePattern(LightPattern):
    particle_positions: List[float] = []
    particle_vels: List[float] = []
    pixels_hsv: List[HSVColor] = []
    particle2_positions: List[float] = []
    particle2_vels: List[float] = []
    pixels2_hsva: List[HSVAColor] = []
    next_particle2_left_in: float = random.uniform(0, 1.5)
    next_particle2_right_in: float = random.uniform(0, 1.5)
    center_glow2_amount: float = 0
    center: float = 80
    radius: float = 200 - 80

    def __init__(self, num_pixels: int):
        super().__init__(num_pixels)

        for i in range(num_pixels):
            self.pixels_hsv.append(colors.BLACK.get_hsv())
            self.pixels2_hsva.append(colors.BLACK.add_alpha().get_hsva())

    def __get_pos_modifier(self, pos: float):
        return abs((self.center - pos) / self.radius)

    def do_main_loop(self, t: float, delta_t: float, palette: Palette):
        if t % 0.3 < delta_t:
            vel = math.copysign(random.uniform(15, 35), t % 0.6 - 0.3)
            self.particle_positions.append(self.center)
            self.particle_vels.append(vel)
        self.next_particle2_left_in -= delta_t
        if self.next_particle2_left_in <= 0:
            vel = -random.uniform(50, 120)
            self.particle2_positions.append(self.center)
            self.particle2_vels.append(vel)
            self.next_particle2_left_in = random.uniform(0.8, 5)
        self.next_particle2_right_in -= delta_t
        if self.next_particle2_right_in <= 0:
            vel = random.uniform(50, 120)
            self.particle2_positions.append(self.center)
            self.particle2_vels.append(vel)
            self.next_particle2_right_in = random.uniform(0.8, 5)

        for i in range(self.num_pixels):
            decay = 4.5 * (1 - 0.5 * self.__get_pos_modifier(i)) * delta_t
            c = self.pixels_hsv[i]
            self.pixels_hsv[i] = HSVColor(c.h, c.s, c.v - c.v * decay)
            c2 = self.pixels2_hsva[i]
            self.pixels2_hsva[i] = HSVAColor(c2.h, c2.s, c2.v, c2.a - c2.a * decay)

        self.center_glow2_amount -= self.center_glow2_amount * 2 * delta_t
        self.center_glow2_amount = max(self.center_glow2_amount, smoothstep(-0.6, 0, -min(self.next_particle2_left_in, self.next_particle2_right_in)))

        removed = 0
        for i in range(len(self.particle_positions)):
            i = i - removed
            pos = self.particle_positions[i]
            vel = self.particle_vels[i]
            delta_x = vel * delta_t * (0.4 + 0.6 * self.__get_pos_modifier(pos))
            r = range(math.floor(pos), math.floor(pos + delta_x)) if vel > 0 else range(math.ceil(pos + delta_x), math.ceil(pos))
            for j in r:
                if 0 <= j < self.num_pixels:
                    c = palette.primary.get_hsv()
                    self.pixels_hsv[j] = HSVColor(
                        c.h,
                        c.s,
                        c.v * (1 + smoothstep(self.center + 0, self.center + 10, j) - smoothstep(self.center - 10, self.center - 0, j))
                    )

            self.particle_positions[i] += delta_x
            if not 0 <= pos < self.num_pixels:
                self.particle_positions.pop(i)
                self.particle_vels.pop(i)
                removed += 1

        removed = 0
        for i in range(len(self.particle2_positions)):
            i = i - removed
            pos = self.particle2_positions[i]
            vel = self.particle2_vels[i]
            delta_x = vel * delta_t * (0.4 + 0.6 * self.__get_pos_modifier(pos))
            r = range(math.floor(pos), math.floor(pos + delta_x)) if vel > 0 else range(math.ceil(pos + delta_x), math.ceil(pos))
            for j in r:
                if 0 <= j < self.num_pixels:
                    self.pixels2_hsva[j] = palette.secondary.get_hsv()\
                        .add_alpha((1 + smoothstep(self.center + 0, self.center + 10, j) - smoothstep(self.center - 10, self.center - 0, j)))

            self.particle2_positions[i] += delta_x
            if not 0 <= pos < self.num_pixels:
                self.particle2_positions.pop(i)
                self.particle2_vels.pop(i)
                removed += 1

        glow_rgb = palette.primary.interp(palette.secondary, self.center_glow2_amount)
        for i in range(self.num_pixels):
            center_glow = (1 + smoothstep(self.center + 0, self.center + 8, i) - smoothstep(self.center - 8, self.center - 0, i))

            self.set_pixel(i,
                self.pixels_hsv[i].interp(glow_rgb, 0.6 * (1 - center_glow)).screen_with(self.pixels2_hsva[i])
            )
