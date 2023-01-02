from typing import List, Tuple

import colors
from colors import RGBColor
from mathfun import rgb_interp
from palette import Palette
from pattern import LightPattern


class LayeredPattern(LightPattern):
    layers: List[LightPattern] = []

    def add_layer(self, layer: LightPattern, position: int = None):
        if position is None:
            self.layers.append(layer)
        else:
            self.layers.insert(position, layer)

    def remove_layer(self, layer: LightPattern):
        self.layers.remove(layer)

    def do_main_loop(self, t: float, delta_t: float, palette: Palette) -> None:
        self.clear()
        for i in range(len(self.layers)):
            frame = self.layers[i].main_loop(t, delta_t, palette)
            self.pixels = [self.pixels[j].rover(frame[j]) for j in range(self.num_pixels)]
