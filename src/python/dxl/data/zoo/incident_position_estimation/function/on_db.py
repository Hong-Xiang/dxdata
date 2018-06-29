from dxl.data.function import Function, function, NestMapOf
from functools import singledispatch
from ..database import orm
from ..data import Hit, Photon, Coincidence
from types import SimpleNamespace
from typing import List
__all__ = ['ToHit', 'ToPhotonFromPhoton',
           'ToPhotonFromHits', 'ToCoincidence', 'processings']


class ToHit(Function):
    def __init__(self, is_crystal_center):
        self.is_crystal_center = is_crystal_center

    def __call__(self, o: orm.Hit) -> Hit:
        if self.is_crystal_center:
            return Hit(o.crystal.x, o.crystal.y, o.crystal.z, o.energy)
        else:
            return Hit(o.x, o.y, o.z, o.energy)


class ToPhotonFromPhoton(Function):
    def __init__(self, to_hit):
        self.to_hit = to_hit

    def __call__(self, p: orm.Photon) -> Photon:
        return Photon([self.to_hit(h) for h in p.hits])


class ToPhotonFromHits(Function):
    def __init__(self, to_hit):
        self.to_hit = to_hit

    def __call__(self, hits: List[orm.Hit]) -> Photon:
        return Photon([self.to_hit(h) for h in hits])


class ToCoincidence(Function):
    def __init__(self, to_hit):
        self.to_hit = to_hit

    def __call__(self, c: orm.Coincidence) -> Coincidence:
        photons = []
        to_photon = ToPhotonFromPhoton(self.to_hit)
        for e in c.events:
            for p in e.photons:
                photons.append(to_photon(p))
        return Coincidence(photons)


class ToPhotonsFromEvents(Function):
    def __init__(self, to_hit):
        self.to_hit = to_hit

    def __call__(self, es: List[orm.Event]) -> Coincidence:
        photons = []
        to_photon = ToPhotonFromPhoton(self.to_hit)
        for e in es:
            for p in e.photons:
                photons.append(to_photon(p))
        return Coincidence(photons)


class processings(SimpleNamespace):
    @classmethod
    def photon(cls, is_crystal_center=True):
        return NestMapOf(ToPhotonFromPhoton(ToHit(is_crystal_center)))

    @classmethod
    def photon_hits(cls, is_crystal_center=True):
        return NestMapOf(ToPhotonFromPhoton(ToHit(is_crystal_center)))

    @classmethod
    def coincidence(cls, is_crystal_center=True):
        return NestMapOf(ToCoincidence(ToHit(is_crystal_center)))

    @classmethod
    def coincidence_events(cls, is_crystal_center=True):
        return NestMapOf(ToPhotonsFromEvents(ToHit(is_crystal_center)))
