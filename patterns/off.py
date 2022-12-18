from LightPattern import LightPattern
from palette import Palette


class OffPattern(LightPattern):

    def get_name(self):
        return 'Lights off'

    def do_main_loop(self, t: float, delta_t: float, palette: Palette):
        pass
