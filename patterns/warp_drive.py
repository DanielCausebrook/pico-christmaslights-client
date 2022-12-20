import colorsys

import math
import random
from typing import List, Tuple

from LightPattern import LightPattern
from mathfun import smoothstep, rgb_interp
from palette import Palette


class WarpDrivePattern(LightPattern):
    particle_positions: List[float] = []
    particle_vels: List[float] = []
    particle_saturations: List[float] = []
    pixels_hsv: List[Tuple[float, float, float]] = []
    particle2_positions: List[float] = []
    particle2_vels: List[float] = []
    particle2_saturations: List[float] = []
    pixels2_hsv: List[Tuple[float, float, float]] = []
    pixels2_alpha: List[float] = []
    next_particle2_left_in: float = random.uniform(0, 1.5)
    next_particle2_right_in: float = random.uniform(0, 1.5)
    center_glow2_amount: float = 0
    center_glow2_hold_time: float = 0
    center: float = 80
    radius: float = 200 - 80

    def __init__(self, num_pixels: int):
        super().__init__(num_pixels)

        for i in range(num_pixels):
            self.pixels_hsv.append((0, 0, 0))
            self.pixels2_hsv.append((0, 0, 0))
            self.pixels2_alpha.append(0)

    def __get_pos_modifier(self, pos: float):
        return abs((self.center - pos) / self.radius)

    def do_main_loop(self, t: float, delta_t: float, palette: Palette):
        if t % 0.3 < delta_t:
            vel = math.copysign(random.uniform(15, 35), t % 0.6 - 0.3)
            self.particle_positions.append(self.center)
            self.particle_vels.append(vel)
            self.particle_saturations.append(random.uniform(0.85, 1))
        self.next_particle2_left_in -= delta_t
        if self.next_particle2_left_in <= 0:
            vel = -random.uniform(50, 120)
            self.particle2_positions.append(self.center)
            self.particle2_vels.append(vel)
            self.particle2_saturations.append(random.uniform(0.85, 1))
            self.next_particle2_left_in = random.uniform(0.8, 5)
            self.center_glow2_hold_time = 0.08
        self.next_particle2_right_in -= delta_t
        if self.next_particle2_right_in <= 0:
            vel = random.uniform(50, 120)
            self.particle2_positions.append(self.center)
            self.particle2_vels.append(vel)
            self.particle2_saturations.append(random.uniform(0.85, 1))
            self.next_particle2_right_in = random.uniform(0.8, 5)
            self.center_glow2_hold_time = 0.08

        for i in range(self.num_pixels):
            self.pixels_hsv[i] = (
                self.pixels_hsv[i][0],
                self.pixels_hsv[i][1],
                self.pixels_hsv[i][2] - self.pixels_hsv[i][2] * 4.5 * (1 - 0.5 * self.__get_pos_modifier(i)) * delta_t
            )
            self.pixels2_alpha[i] -= self.pixels2_alpha[i] * 4.5 * (1 - 0.5 * self.__get_pos_modifier(i)) * delta_t

        if self.center_glow2_hold_time > 0:
            self.center_glow2_hold_time -= delta_t
        # else:
        self.center_glow2_amount -= self.center_glow2_amount * 4 * delta_t
        self.center_glow2_amount = max(self.center_glow2_amount, smoothstep(-0.3, 0, -min(self.next_particle2_left_in, self.next_particle2_right_in)))

        removed = 0
        for i in range(len(self.particle_positions)):
            i = i - removed
            pos = self.particle_positions[i]
            vel = self.particle_vels[i]
            delta_x = vel * delta_t * (0.4 + 0.6 * self.__get_pos_modifier(pos))
            r = range(math.floor(pos), math.floor(pos + delta_x)) if vel > 0 else range(math.ceil(pos + delta_x), math.ceil(pos))
            for j in r:
                if 0 <= j < self.num_pixels:
                    rgb = colorsys.rgb_to_hsv(*palette.primary)
                    rgb = (
                        rgb[0],
                        rgb[1] * self.particle_saturations[i],
                        rgb[2] * (1 + smoothstep(self.center + 0, self.center + 10, j) - smoothstep(self.center - 10, self.center - 0, j))
                    )
                    self.pixels_hsv[j] = rgb

            self.particle_positions[i] += delta_x
            if not 0 <= pos < self.num_pixels:
                self.particle_positions.pop(i)
                self.particle_vels.pop(i)
                self.particle_saturations.pop(i)
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
                    rgb = colorsys.rgb_to_hsv(*palette.secondary)
                    rgb = (
                        rgb[0],
                        rgb[1] * self.particle2_saturations[i],
                        rgb[2]
                    )
                    self.pixels2_alpha[j] = (1 + smoothstep(self.center + 0, self.center + 10, j) - smoothstep(self.center - 10, self.center - 0, j))
                    self.pixels2_hsv[j] = rgb

            self.particle2_positions[i] += delta_x
            if not 0 <= pos < self.num_pixels:
                self.particle2_positions.pop(i)
                self.particle2_vels.pop(i)
                self.particle2_saturations.pop(i)
                removed += 1

        glow_rgb = rgb_interp(palette.primary, palette.secondary, self.center_glow2_amount)
        for i in range(self.num_pixels):
            rgb1 = colorsys.hsv_to_rgb(*self.pixels_hsv[i])
            rgb2 = colorsys.hsv_to_rgb(*self.pixels2_hsv[i])
            alpha2 = self.pixels2_alpha[i]

            center_glow = (1 + smoothstep(self.center + 0, self.center + 8, i) - smoothstep(self.center - 8, self.center - 0, i))
            rgb = rgb_interp(rgb1, glow_rgb, 0.6 * (1 - center_glow))
            rgb = rgb_interp(rgb, rgb2, alpha2)

            self.set_pixel_rgb(i, *rgb)
