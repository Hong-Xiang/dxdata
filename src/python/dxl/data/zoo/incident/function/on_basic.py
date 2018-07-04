from dxl.data.function import (Function, function, x, MapByPosition,
                               MapWithUnpackArgsKwargs, To, Padding,
                               Swap, append, NestMapOf, concatenate,
                               Filter)
import numpy as np
import random

from typing import List
from ..data import Hit, ShuffledHits, ShuffledCoincidenceHits, Photon, Coincidence


class ShuffleHits(Function):
    def __call__(self, photon: Photon):
        hits = photon.hits
        order = self.order(hits)
        return photon.update(hits=[hits[i] for i in order], first_hit_index=order.index(0))


class RandomShuffleHits(ShuffleHits):
    def order(self, hits):
        order = list(range(len(hits)))
        random.shuffle(order)
        return order


random_shuffle_hits = RandomShuffleHits()


class JustAddIndex(ShuffleHits):
    def order(self, hits):
        return list(range(len(hits)))


just_add_index = JustAddIndex()


class SortHitsByEnergy(ShuffleHits):
    def order(self, hits):
        energy = np.array([h.e for h in hits])
        order = list(np.argsort(energy))
        return order


sort_hits_by_energy = SortHitsByEnergy()


__all__ = ['random_shuffle_hits', 'just_add_index', 'sort_hits_by_energy']


class PaddingPhoton(Function):
    def __init__(self, padding_size):
        self.padding = Padding(padding_size, is_with_padded_size=False)

    def __call__(self, p: Photon):
        return p.update(hits=self.padding(p.hits),
                        nb_true_hits=len(p.hits))


@function
def swap_photon(c: Coincidence):
    return Coincidence([c.snd, c.fst] + c.photons[2:])


# def photon2shuffled_hits(padding_size: int, shuffle: ShuffledHits):
#     return (x.hits
#             >> shuffle
#             >> MapByPosition(0, To(np.array)
#                              >> Padding(padding_size, is_with_padded_size=True))
#             >> MapWithUnpackArgsKwargs(append)
#             >> Swap(1, 2)
#             >> MapWithUnpackArgsKwargs(To(ShuffledHits)))


# @function
# def _merge_helper(shuffled_hits_list):
#     sh0, sh1 = shuffled_hits_list
#     hits0, hits1 = sh0.hits, sh1.hits
#     hits = concatenate([hits0, hits1], 1)
#     return ShuffledCoincidenceHits(hits, sh0.first_hit_index, sh0.padded_size)


# def coincidence2shuffled_hits(padding_size: int, shuffle: ShuffledHits):
#     return (x.photons
#             >> NestMapOf(photon2shuffled_hits(padding_size, shuffle))
#             >> _merge_helper)


# __all__ += ['photon2shuffled_hits', 'coincidence2shuffled_hits']
