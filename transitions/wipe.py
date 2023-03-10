from pattern import LightPattern
from pattern_blended import BlendedPattern
from mathfun import smoothstep
from palette import Palette
from transition import Transition, TransitionFactory


class WipeTransitionFactory(TransitionFactory):
    def __init__(self, softness: float = 0, reverse: bool = False):
        self.softness = softness
        self.reverse = reverse

    def new_transition(self, num_pixels: int, pattern1: LightPattern, pattern2: LightPattern, duration_s: float):
        return WipeTransition(num_pixels, pattern1, pattern2, duration_s, self.softness, self.reverse)

    def get_name(self):
        return 'Wipe'


class WipeTransition(Transition):
    duration_s: float
    softness: float
    blended_pattern: BlendedPattern
    reverse: bool

    def __init__(self, num_pixels: int, pattern1: LightPattern, pattern2: LightPattern, duration_s: float, softness: float = 0, reverse: bool = False):
        super().__init__(num_pixels, pattern1, pattern2, duration_s)

        self.duration_s = duration_s
        self.softness = softness
        self.reverse = reverse
        self.blended_pattern = BlendedPattern(num_pixels, [pattern1, pattern2])
        self.blended_pattern.set_mix([1, 0])

    def do_main_loop(self, t: float, delta_t: float, palette: Palette):
        if not self.reverse:
            wipe_pos = (self.num_pixels + self.softness) * self.progress - self.softness/2
        else:
            wipe_pos = (self.num_pixels + self.softness) * (1 - self.progress) - self.softness/2

        for p in range(self.num_pixels):
            amount = smoothstep(wipe_pos - self.softness/2, wipe_pos + self.softness/2, p)
            if not self.reverse:
                self.blended_pattern.set_pixel_mix(p, [amount, 1-amount])
            else:
                self.blended_pattern.set_pixel_mix(p, [1-amount, amount])

        self.pixels = self.blended_pattern.main_loop(t, delta_t, palette)
