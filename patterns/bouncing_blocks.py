import math
import random

import colors
from colors import HSVColor
from effects.persistence import PersistenceEffect
from pattern import LightPattern
import numpy as np

from palette import Palette
from patterns.gentle_2tone import Gentle2TonePattern
import mathfun


class BouncingBlocksPattern(LightPattern):

    def __init__(self, num_pixels, seed_bg=0):
        super().__init__(num_pixels)

        self.numCars = round(num_pixels / 8)
        self.carHues = np.zeros(self.numCars)
        self.carPos = np.zeros(self.numCars)
        self.carVels = np.zeros(self.numCars)
        self.carSizes = np.ones(self.numCars)
        self.carHeat = np.zeros(self.numCars)
        for c in range(self.numCars):
            self.carPos[c] = random.randint(0, num_pixels - 1)
            self.carVels[c] = random.uniform(-20, 30)
            self.carHues[c] = random.uniform(0, 1)
            self.carSizes[c] = random.randint(1, 5)

        # self.gentle_bg = Gentle2TonePattern(num_pixels, speed=0.5, gradient_width=0.4, seed=seed_bg)

        self.add_effect(PersistenceEffect(num_pixels, 3))

    def get_name(self):
        return 'Bouncing Blocks'

    def do_main_loop(self, t: float, delta_t: float, palette: Palette):
        self.clear()

        # bg_palette = Palette(palette.primary.dim(0.6), palette.secondary.dim(0.6), palette.accent)
        # self.pixels = self.gentle_bg.main_loop(t, delta_t, bg_palette)

        for i in range(self.numCars):
            self.carPos[i] += delta_t * self.carVels[i]
            self.carPos[i] = self.carPos[i] % self.num_pixels
            self.carHeat[i] -= delta_t
            for j in range(i + 1, self.numCars):
                if abs(self.carPos[i] - self.carPos[j]) < (self.carSizes[i]/2) + (self.carSizes[j]/2) and math.copysign(1, self.carPos[i] - self.carPos[j]) != math.copysign(1, self.carVels[i] - self.carVels[j]):
                    vi = self.carVels[i]
                    vj = self.carVels[j]
                    mi = self.carSizes[i]
                    mj = self.carSizes[j]
                    self.carVels[i] = (((mi - mj) / (mi + mj)) * vi) + (((2 * mj) / (mi + mj)) * vj)
                    self.carVels[j] = (((2 * mi) / (mi + mj)) * vi) + (((mj - mi) / (mi + mj)) * vj)
                    self.carHeat[i] += (0.9 - self.carHeat[i]) / 6
                    self.carHeat[j] += (0.9 - self.carHeat[j]) / 6
            if self.carHeat[i] < 0:
                self.carHeat[i] = 0
            elif self.carHeat[i] > 1:
                self.carHeat[i] = 1
            for x in range(round(self.carPos[i] - (self.carSizes[i]/2)), round(self.carPos[i] + (self.carSizes[i]/2))):
                self.set_pixel((x + self.num_pixels) % self.num_pixels, HSVColor(self.carHues[i], 1 - self.carHeat[i], 1))
