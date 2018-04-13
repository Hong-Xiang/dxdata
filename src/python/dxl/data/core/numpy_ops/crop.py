import numpy as np
from typing import Iterable, Tuple


def crop(data: np.ndarray,
         crop_sizes: Iterable[Tuple[int, int]]) -> np.ndarray:
    """
    """
    def expand_ints(crop_sizes):
      result = []
      for cs = crop_sizes:
        if cs is None:
          result.append((0, 0))
        elif isinstance(cs, int):
          result.append((cs, cs))
        else:
          result.append(cs)
      return result
