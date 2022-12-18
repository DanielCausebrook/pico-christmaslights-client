from typing import List

from LightPattern import LightPattern
import mathfun


class BlendedPattern(LightPattern):
    patterns: List[LightPattern]
    pixel_mixes: List[List[float]]

    def __init__(self, num_pixels, patterns):
        """
        :param int num_pixels:
        :param LightPattern[] patterns:
        """
        super().__init__(num_pixels)
        self.patterns = patterns
        self.pixel_mixes = []
        for _ in range(num_pixels):
            mix = []
            for _ in patterns:
                mix.append(0)
            self.pixel_mixes.append(mix)

    def set_mix(self, mix):
        for pixel in range(self.num_pixels):
            self.pixel_mixes[pixel] = mix

    def set_pixel_mix(self, pixel, mix):
        self.pixel_mixes[pixel] = mix

    def do_main_loop(self, t, delta_t, palette):
        frames = []
        for pattern_index in range(len(self.patterns)):
            self.patterns[pattern_index].main_loop(t, delta_t, palette)
            frames.append(self.patterns[pattern_index].get_frame())

        for pixel in range(self.num_pixels):
            total_weight = 0
            r_sum = 0
            g_sum = 0
            b_sum = 0

            for pattern_index in range(len(self.patterns)):
                rgb = frames[pattern_index][pixel]
                weight = self.pixel_mixes[pixel][pattern_index]
                total_weight += weight
                r_sum += mathfun.rgb_component_to_linear(rgb[0]) * weight
                g_sum += mathfun.rgb_component_to_linear(rgb[1]) * weight
                b_sum += mathfun.rgb_component_to_linear(rgb[2]) * weight

            if total_weight > 1:
                r_sum /= total_weight
                g_sum /= total_weight
                b_sum /= total_weight

            self.set_pixel_rgb(
                pixel,
                mathfun.rgb_component_from_linear(r_sum),
                mathfun.rgb_component_from_linear(g_sum),
                mathfun.rgb_component_from_linear(b_sum)
            )
