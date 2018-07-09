from dxl.data.function import (Function, function)
import numpy as np
import random

from typing import List
from ..data import Hit, ShuffledHits, ShuffledCoincidenceHits, Photon, Coincidence

MAX_CRYSTAL_INDEX = 999999

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


class PaddingPhoton(Function):
    def __init__(self, padding_size):
        self.padded_size = padding_size

    def __call__(self, p: Photon):
        if len(p.hits) > self.padded_size:
            return p.update()
        hits = [h for h in p.hits]
        hits += [p.hits[0].update(x=0.0, y=0.0, z=0.0, e=0.0, crystal_index=MAX_CRYSTAL_INDEX)
                 for _ in range(self.padded_size - len(p.hits))]
        return p.update(hits=hits,
                        nb_true_hits=len(p.hits))


@function
def swap_photon(c: Coincidence):
    return Coincidence([c.snd, c.fst] + c.photons[2:])


__all__ = ['random_shuffle_hits', 'just_add_index',
           'sort_hits_by_energy', 'PaddingPhoton', 'swap_photon']
