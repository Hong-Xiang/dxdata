import random
import typing
from contextlib import contextmanager
from functools import lru_cache
from typing import List

import numpy as np

import tqdm
from dxl.data.core import Columns
from dxl.data.database import get_or_create_session, DBScannerWith, ChunkedDBScannerWith
from dxl.data.function import (Function, function, GetAttr, NestMapOf,
                               OnIterator, To, MapByNameOf, Padding,
                               append, MapWithUnpackArgsKwargs, MapByPosition,
                               Swap)


from . import orm
from .query import all_photon, nb_photon, first_photon


# TODO: Use NamedTuple, mingrating to data class in 3.7

__all__ = ['Hit', 'HitWithCrystalCenter', 'Photon', 'PhotonColumns']


class TensorTypes:
    @classmethod
    def dtypes(cls):
        raise NotImplementedError

    @classmethod
    def shapes(cls):
        raise NotImplementedError


class Hit(typing.NamedTuple, TensorTypes):
    x: np.float32
    y: np.float32
    z: np.float32
    e: np.float32

    @classmethod
    def from_orm(cls, o: orm.Hit):
        return Hit(o.x, o.y, o.z, o.energy)

    @classmethod
    def dtypes(cls):
        return cls._field_types

    @classmethod
    def shapes(cls):
        return {k: [] for k in cls.dtypes}


class HitWithCrystalCenter(Hit):
    @classmethod
    def from_orm(cls, o: orm.Hit):
        return Hit(o.crystal.x, o.crystal.y, o.crystal.z, o.energy)


class Photon(typing.NamedTuple, TensorTypes):
    hits: List[Hit]

    @classmethod
    def dtypes(cls):
        return {k: Hit for k in cls._field_types}

    @classmethod
    def shapes(cls):
        return {k: [None] for k in cls._field_types}


class PhotonColumns(Columns):
    def __init__(self, path, hit_dataclass, is_chunked=False):
        super().__init__(Photon)
        self.path = path
        self.hit_dataclass = hit_dataclass
        self.is_chunked = is_chunked

    @property
    @lru_cache(1)
    def capacity(self):
        return nb_photon(self.path)

    def _make_db_scanner(self):
        process = (GetAttr('hits')
                   >> NestMapOf(ORMTo(self.hit_dataclass))
                   >> To(Photon))
        if self.is_chunked:
            process = NestMapOf(process)
            scanner_type = ChunkedDBScannerWith
        else:
            scanner_type = DBScannerWith
        return scanner_type(self.path, first_photon >> MapByPosition(0, process))

    def __iter__(self):
        return iter(self._make_db_scanner())

    @property
    def dtypes(self):
        return {'hits': self.hit_dataclass}

        # def make_iterator():

        #     for p in all_photon(self.path):
        #         yield Photon(list(p.hits))

        # return make_iterator()


class ShuffledHitsWithIndex(typing.NamedTuple, TensorTypes):
    hits: List[Hit]
    first_hit_index: np.int32

    @classmethod
    def shapes(cls):
        return {'hits': [None, 4], 'first_hit_index': []}

    @classmethod
    def dtypes(cls):
        return {'hits': np.float32, 'first_hit_index': np.int32}


class ShuffledHitsWithIndexAndPaddedSize(typing.NamedTuple, TensorTypes):
    hits: List[Hit]
    first_hit_index: np.int32
    padded_size: np.int32

    @classmethod
    def shapes(cls):
        return {'hits': [None, 4], 'first_hit_index': [], 'padded_size': []}

    @classmethod
    def dtypes(cls):
        return {'hits': np.float32, 'first_hit_index': np.int32, 'padded_size': np.int32}


__all__ += ['ShuffledHitsWithIndex', 'ShuffledHitsWithIndexAndPaddedSize']


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

__all__ += ['random_shuffle_hits', 'just_add_index', 'sort_hits_by_energy']


class ORMTo(Function):
    def __init__(self, dataclass):
        self.dataclass = dataclass

    def __call__(self, o):
        return self.dataclass.from_orm(o)


class ShuffledHitsColumns(Columns):
    def __init__(self, source_columns: Columns, dataclass, processing):
        super().__init__(dataclass)
        self.source_columns = source_columns
        self.processing = processing

    @property
    def capacity(self):
        return self.source_columns.capacity

    def __iter__(self):
        return self.processing(self.source_columns)


def padded_hits_columns(path, size, hit_dataclass, shuffle, is_with_padded_size):
    process = (GetAttr('hits')
               >> shuffle
               >> MapByPosition(0, To(np.array))
               >> MapByPosition(0, Padding(size, is_with_padded_size=is_with_padded_size)))
    if is_with_padded_size:
        process = (process >> MapWithUnpackArgsKwargs(append) >> Swap(1, 2))
        dataclass = ShuffledHitsWithIndexAndPaddedSize
    else:
        dataclass = ShuffledHitsWithIndex
    process = process >> MapWithUnpackArgsKwargs(To(dataclass))
    return ShuffledHitsColumns(PhotonColumns(path, hit_dataclass), dataclass, OnIterator(process))


__all__ += ['ORMTo', 'ShuffledHitsColumns', 'padded_hits_columns']
