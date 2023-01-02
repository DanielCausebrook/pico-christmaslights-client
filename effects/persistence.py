from typing import List

from colors import Color, RGBColor
from effect import Effect


class PersistenceEffect(Effect):
    num_pixels: int
    decay_rate: float
    pixel_colors: List[Color]
    pixel_alphas: List[float]

    def __init__(self, num_pixels: int, decay_rate: float):
        self.num_pixels = num_pixels
        self.decay_rate = decay_rate
        self.pixel_colors = [RGBColor(0.0, 0.0, 0.0) for _ in range(num_pixels)]
        self.pixel_alphas = [0.0 for _ in range(num_pixels)]

    def apply_main_loop(self, frame: List[Color], t: float, delta_t: float) -> List[Color]:
        self.pixel_colors = [self.pixel_colors[i] if frame[i].get_alpha() == 0 else frame[i] for i in range(self.num_pixels)]
        self.pixel_alphas = [min(max(frame[i].get_alpha(), self.pixel_alphas[i] - self.decay_rate * self.pixel_alphas[i] * delta_t, 0), 1) for i in range(self.num_pixels)]
        return [self.pixel_colors[i].set_alpha(self.pixel_alphas[i]) for i in range(self.num_pixels)]
