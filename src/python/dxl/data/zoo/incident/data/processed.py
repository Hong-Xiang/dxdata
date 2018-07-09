from typing import List, NamedTuple
from .basic import TensorTypes, Hit
import numpy as np


class ShuffledHits(NamedTuple, TensorTypes):
    hits: List[Hit]
    first_hit_index: np.int32
    padded_size: np.int32

    @classmethod
    def shapes(cls):
        return {'hits': [None, 4], 'first_hit_index': [], 'padded_size': []}

    @classmethod
    def dtypes(cls):
        return {'hits': np.float32, 'first_hit_index': np.int32, 'padded_size': np.int32}


class ShuffledCoincidenceHits(NamedTuple, TensorTypes):
    hits: List[Hit]
    first_hit_index: np.int32
    padded_size: np.int32

    @classmethod
    def shapes(cls):
        return {'hits': [None, 8], 'first_hit_index': [], 'padded_size': []}

    @classmethod
    def dtypes(cls):
        return {'hits': np.float32, 'first_hit_index': np.int32, 'padded_size': np.int32}


__all__ = ['ShuffledHits', 'ShuffledCoincidenceHits']
