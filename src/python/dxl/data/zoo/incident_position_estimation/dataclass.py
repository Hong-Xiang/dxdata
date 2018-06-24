from dxl.data.database import get_or_create_session
from dxl.data.core import Columns
import tqdm
import numpy as np
from .query import nb_photon, all_photon
from contextlib import contextmanager
from functools import lru_cache
import random
from . import orm
from typing import List

dataset_path = '../../../data/gamma.db'

# TODO: Use NamedTuple, mingrating to data class in 3.7

import typing


from dxl.data.function import function, Function


class TensorTypes:
    def dtypes(self):
        raise NotImplementedError

    def shapes(self):
        raise NotImplementedError


class Hit(typing.NamedTuple, TensorTypes):
    x: np.float32
    y: np.float32
    z: np.float32
    e: np.float32

    @classmethod
    def from_orm(cls, o: orm.Hit):
        return Hit(o.x, o.y, o.z, o.energy)

    @property
    def dtypes(self):
        return self._field_types

    @property
    def shapes(self):
        return {k: [] for k in self.dtypes}


class HitWithCrystalCenter(Hit):
    @classmethod
    def from_orm(cls, o: orm.Hit):
        return Hit(o.crystal.x, o.crystal.y, o.crystal.z, o.energy)


class Photon(typing.NamedTuple, TensorTypes):
    hits: List[orm.Hit]

    @property
    def dtypes(self):
        return {k: orm.Hit for k in self._field_types}

    @property
    def shapes(self):
        return {k: [None] for k in self._field_types}


class PhotonColumns(Columns):
    def __init__(self, path):
        super().__init__(Photon)
        self.path = path
        self.session = get_or_create_session(self.path)

    # def _process(self, data):
    #     if isinstance(data, str):
    #         path = data
    #         is_shuffle = True
    #     else:
    #         path = data['path']
    #         is_shuffle = data['is_shuffle']
    #     self.is_shuffle = is_shuffle
    #     self.is_crystal_center = data['is_crystal_center']
    #     return get_or_create_session(path)

    @property
    def types(self):
        return (np.float32, np.int32)

    @property
    def shapes(self):
        return ([None, 4], [None])

    @property
    def columns(self):
        return ('hits', 'first_hit')

    @property
    @lru_cache(1)
    def capacity(self):
        return nb_photon()

    def __iter__(self):
        def make_iterator():
            for p in all_photon(self.session):
                yield Photon(list(p.hits))

        return make_iterator()


class ShuffledHitsWithIndex(typing.NamedTuple, TensorTypes):
    hits: List[Hit]
    first_hit_index: np.int32

    @property
    def shapes(self):
        return {'hits': [None, 4], 'first_hit_index': [None]}

    @property
    def dtypes(self):
        return {'hits': np.float32, 'first_hit_index': np.int32}


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


class ORMTo(Function):
    def __init__(self, dataclass):
        self.dataclass = dataclass

    def __call__(self, o):
        return self.dataclass.from_orm(o)
