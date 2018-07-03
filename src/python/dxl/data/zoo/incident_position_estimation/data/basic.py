import random
from contextlib import contextmanager
from functools import lru_cache
from typing import List, NamedTuple

import numpy as np

import tqdm
from dxl.data.function import (Function, function, GetAttr, NestMapOf,
                               OnIterator, To, MapByNameOf, Padding,
                               append, MapWithUnpackArgsKwargs, MapByPosition,
                               Swap, x)


# TODO: Use NamedTuple, mingrating to data class in 3.7

__all__ = ['Hit', 'Photon', 'Coincidence']


class TensorTypes:
    @classmethod
    def dtypes(cls):
        raise NotImplementedError

    @classmethod
    def shapes(cls):
        raise NotImplementedError


class Hit(NamedTuple, TensorTypes):
    x: np.float32
    y: np.float32
    z: np.float32
    e: np.float32

    @classmethod
    def dtypes(cls):
        return cls._field_types

    @classmethod
    def shapes(cls):
        return {k: [] for k in cls.dtypes}


class Photon(NamedTuple):
    hits: List[Hit]


class Coincidence(NamedTuple):
    photons: List[Photon]


# def padded_hits_columns(path, size, hit_dataclass, shuffle, is_with_padded_size):
#     process = (GetAttr('hits')
#                >> shuffle
#                >> MapByPosition(0, To(np.array))
#                >> MapByPosition(0, Padding(size, is_with_padded_size=is_with_padded_size)))
#     if is_with_padded_size:
#         process = (process >> MapWithUnpackArgsKwargs(append) >> Swap(1, 2))
#         dataclass = ShuffledHitsWithIndexAndPaddedSize
#     else:
#         dataclass = ShuffledHitsWithIndex
#     process = process >> MapWithUnpackArgsKwargs(To(dataclass))
#     return ShuffledHitsColumns(PhotonColumns(path, hit_dataclass), dataclass, OnIterator(process))


# __all__ += ['ORMTo', 'ShuffledHitsColumns', 'padded_hits_columns']
