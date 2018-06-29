from dxl.data.function import Function, x, MapByPosition, MapWithUnpackArgsKwargs, To, Padding, Swap
from ..data.precessed import ShuffledHitsWithIndexAndPaddedSize
import numpy as np
import random

from typing import List
from ..data import Hit, HitWithCrystalCenter


class ShuffleHits(Function):
    def make_result(self, hits, order):
        first_index = order.index(0)
        return type(hits)([hits[i] for i in order]), first_index


class RandomShuffleHits(ShuffleHits):
    def __call__(self, hits):
        order = list(range(len(hits)))
        random.shuffle(order)
        return self.make_result(hits, order)


random_shuffle_hits = RandomShuffleHits()


class JustAddIndex(ShuffleHits):
    def __call__(self, hits):
        return self.make_result(hits, list(range(len(hits))))


just_add_index = JustAddIndex()


class SortHitsByEnergy(ShuffleHits):
    def __call__(self, hits):
        energy = np.array([h.e for h in hits])
        order = list(np.argsort(energy))
        return self.make_result(hits, order)


sort_hits_by_energy = SortHitsByEnergy()


__all__ = ['random_shuffle_hits', 'just_add_index', 'sort_hits_by_energy']


def photon2shuffled_hits(shuffle: ShuffleHits, padding_size: int):
    return (x.hits
            >> shuffle
            >> MapByPosition(0, To(np.array)
                             >> Padding(padding_size, is_with_padded_size=True))
            >> MapWithUnpackArgsKwargs(append)
            >> Swap(1, 2)
            >> MapWithUnpackArgsKwargs(To(ShuffledHitsWithIndexAndPaddedSize)))


__all__ += ['photon2shuffled_hits']
