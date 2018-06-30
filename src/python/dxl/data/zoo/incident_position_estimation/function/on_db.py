from dxl.data.function import Function, function, NestMapOf
from functools import singledispatch
from ..database import orm
from ..data import Hit, Photon, Coincidence
from types import SimpleNamespace
from typing import List
__all__ = ['ToHit', 'ToPhoton', 'ToCoincidence', 'processings']


class ToHit(Function):
    def __init__(self, is_crystal_center):
        self.is_crystal_center = is_crystal_center

    def __call__(self, o: orm.Hit) -> Hit:
        if self.is_crystal_center:
            return Hit(o.crystal.x, o.crystal.y, o.crystal.z, o.energy)
        else:
            return Hit(o.x, o.y, o.z, o.energy)


class ToPhoton(Function):
    def __init__(self, to_hit):
        self.to_hit = to_hit

    def __call__(self, p: orm.Photon) -> Photon:
        return Photon([self.to_hit(h) for h in p.hits])


class ToCoincidence(Function):
    def __init__(self, to_hit):
        self.to_hit = to_hit

    def __call__(self, c: orm.Coincidence) -> Coincidence:
        photons = []
        to_photon = ToPhoton(self.to_hit)
        for e in c.events:
            for p in e.photons:
                photons.append(to_photon(p))
        return Coincidence(photons)


class processings(SimpleNamespace):
    @classmethod
    def photon(cls, is_crystal_center=True):
        return NestMapOf(ToPhoton(ToHit(is_crystal_center)))

    @classmethod
    def coincidence(cls, is_crystal_center=True):
        return NestMapOf(ToCoincidence(ToHit(is_crystal_center)))
