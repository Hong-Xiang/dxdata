from typing import NamedTuple
import numpy as np

from abc import ABC

class Scanner(ABC):
    def get_crystal_id(self, p: np.array) -> int:
        pass
    
    def get_event_position(self, cid: int) -> np.array:
        pass

class ECATScanner(NamedTuple):
    ...