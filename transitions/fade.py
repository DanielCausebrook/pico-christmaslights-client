from LightPattern import LightPattern
from mathfun import rgb_interp
from palette import Palette
from transition import Transition


class FadeTransition(Transition):
    duration_s: float

    def __init__(self, num_pixels: int, pattern1: LightPattern, pattern2: LightPattern, duration_s: float):
        super().__init__(num_pixels, pattern1, pattern2, duration_s)

        self.duration_s = duration_s

    def do_main_loop(self, t: float, delta_t: float, palette: Palette):
        frame1 = self.pattern1.main_loop(t, delta_t, palette)
        frame2 = self.pattern2.main_loop(t, delta_t, palette)
        self.pixels = [rgb_interp(frame1[p], frame2[p], self.get_progress()) for p in range(self.num_pixels)]
