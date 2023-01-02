from abc import ABC, abstractmethod
from typing import List

from colors import Color


class Effect(ABC):
    @abstractmethod
    def apply_main_loop(self, frame: List[Color], t: float, delta_t: float) -> List[Color]:
        pass
