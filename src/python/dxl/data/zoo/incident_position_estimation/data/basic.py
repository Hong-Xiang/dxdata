from typing import List, NamedTuple
import numpy as np
# TODO: Use NamedTuple, mingrating to data class in 3.7

__all__ = ['Hit', 'Photon', 'Coincidence']


class TensorTypes:
    @classmethod
    def dtypes(cls):
        raise NotImplementedError

    @classmethod
    def shapes(cls):
        raise NotImplementedError


def _formatter_with_none_support(o, fields):
    result = "<{}(".format(o.__class__)
    for i, n in enumerate(fields):
        value = getattr(o, n)
        if value is None:
            continue
        result += "{}={}".format(o, value)
        if i < len(fields) - 1:
            result += ", "
    result += ")>"
    return result


class Hit:
    def __init__(self, x: float=0.0, y: float=0.0, z: float=0.0, e: float=0.0, crystal_index: int=None):
        self.x = x
        self.y = y
        self.z = z
        self.e = e
        self.crystal_index = crystal_index

    def dtypes(self):
        result = {'x': np.float32, 'y': np.float32,
                  'z': np.float32, 'e': np.float32}
        if self.crystal_index is not None:
            result['crystal_index'] = np.int32

    def shapes(self):
        result = {'x': [], 'y': [], 'z': [], 'e': []}
        if self.crystal_index is not None:
            result['crystal_index'] = []

    def __repr__(self):
        return _formatter_with_none_support(self, ['x', 'y', 'z', 'e', 'crystal_index'])

    def update(self, x=..., y=..., z=..., e=..., crystal_index=...):
        return Hit(
            x if x is not ... else self.x,
            y if y is not ... else self.y,
            z if z is not ... else self.z,
            e if e is not ... else self.e,
            crystal_index if crystal_index is not ... else self.crystal_index
        )


class Photon:
    def __init__(self, hits: List[Hit], first_hit_index: int=None, nb_true_hits: int=None):
        self.hits = hits
        self.first_hit_index = first_hit_index
        self.nb_true_hits = nb_true_hits

    def __repr__(self):
        return _formatter_with_none_support(self, ['hits', 'first_hit_index', 'nb_true_hits'])

    def update(self, hits=..., first_hit_index=..., nb_true_hits=...):
        return Photon(
            hits if hits is not ... else self.hits,
            first_hit_index if first_hit_index is not ... else self.first_hit_index,
            nb_true_hits if nb_true_hits is not ... else self.nb_true_hits
        )


class Coincidence:
    def __init__(self, photons):
        self.photons = photons

    @property
    def fst(self):
        return self.photons[0]

    @property
    def snd(self):
        return self.photons[1]

    def __repr__(self):
        return "<{}(photons={})>".format(self.__class__, self.photons)
