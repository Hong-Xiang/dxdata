from typing import NamedTuple
import numpy as np


def get_crystal_id(point, scanner):
    ...


def get_event_position(crystal_id, scanner):
    ...


class ListModeLoR(NamedTuple):
    point0: np.array
    point1: np.array
    value: float = 1.0

    def to_sinogram(self, scanner):
        return SinogramLoR(scanner.get_crystal_id(self.point0),
                           scanner.get_crystal_id(self.point1),
                           self.value)


class SinogramLoR(NamedTuple):
    crystal0: int
    crystal1: int
    value: float

    def to_list_mode(self, scanner):
        return ListModeLoR(scanner.get_event_position(self.crystal0),
                           scanner.get_event_position(self.crystal1),
                           self.value)
