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


def _formatter_with_none_support(typename, o, fields):
    result = "<{}(".format(typename)
    with_prev = False
    for i, n in enumerate(fields):
        value = getattr(o, n)
        if value is None:
            continue
        if with_prev:
            result += ", "
        result += "{}={}".format(n, value)
        with_prev = True
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

    @property
    def _fields(self):
        result = ['x', 'y', 'z', 'y', 'e']
        if self.crystal_index is not None:
            result.append('crystal_index')
        return tuple(result)
    
    def __getitem__(self, index):
        return [self.x, self.y, self.z, self.e, self.crystal_index][index]

    def __repr__(self):
        return _formatter_with_none_support('Hit', self, ['x', 'y', 'z', 'e', 'crystal_index'])

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

    @property
    def _fields(self):
        result = ['hits']
        if self.first_hit_index is not None:
            result.append('first_hit_index')
        if self.nb_true_hits is not None:
            result.append('nb_true_hits')
        return tuple(result)

    def __repr__(self):
        return _formatter_with_none_support('Photon', self, ['hits', 'first_hit_index', 'nb_true_hits'])

    def update(self, hits=..., first_hit_index=..., nb_true_hits=...):
        return Photon(
            hits if hits is not ... else self.hits,
            first_hit_index if first_hit_index is not ... else self.first_hit_index,
            nb_true_hits if nb_true_hits is not ... else self.nb_true_hits
        )
    
    def __getitem__(self, index):
        return [self.hits, self.first_hit_index, self.nb_true_hits][index]


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
        return "<Coincidence(photons={})>".format(self.photons)

    @property
    def _fields(self):
        return ('photons',)

    def __getitem__(self, index):
        return [self.photons][index]