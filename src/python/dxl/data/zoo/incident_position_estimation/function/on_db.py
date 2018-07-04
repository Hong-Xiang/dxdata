from dxl.data.function import Function, function, NestMapOf
from functools import singledispatch
from ..database import orm, chunked, nb
from ..data import Hit, Photon, Coincidence, QuerySpec, FeatureSpec
from types import SimpleNamespace
from typing import List

__all__ = ['ToHit', 'ToPhoton', 'ToCoincidence',
           'processings', 'load', 'load_all']


class ToHit(Function):
    def __init__(self, feature_spec: FeatureSpec):
        self.spec = feature_spec

    def __call__(self, o: orm.Hit) -> Hit:
        if self.spec.is_crystal_center:
            x, y, z = o.crystal.x, o.crystal.y, o.crystal.z
        else:
            x, y, z = o.x, o.y, o.z
        cid = o.crystal_id if self.spec.is_crystal_index else None
        return Hit(o.x, o.y, o.z, o.energy, cid)


class ToPhoton(Function):
    def __init__(self, spec: FeatureSpec):
        self.to_hit = ToHit(spec)

    def __call__(self, p: orm.Photon) -> Photon:
        return Photon([self.to_hit(h) for h in p.hits])


class ToCoincidence(Function):
    def __init__(self, spec: FeatureSpec):
        self.to_photon = ToPhoton(spec)

    def __call__(self, c: orm.Coincidence) -> Coincidence:
        photons = []
        for e in c.events:
            for p in e.photons:
                photons.append(self.to_photon(p))
        return Coincidence(photons)


class processings(SimpleNamespace):
    @classmethod
    def photon(cls, spec: FeatureSpec):
        return NestMapOf(ToPhoton(ToHit(spec)))

    @classmethod
    def coincidence(cls, spec: FeatureSpec):
        return NestMapOf(ToCoincidence(ToHit(spec)))


class load(SimpleNamespace):
    @classmethod
    def photon(cls, query_sepc: QuerySpec, feature_spec: FeatureSpec):
        return chunked.photon(query_sepc.path,
                              processings.photon(feature_spec),
                              query_sepc.limit,
                              query_sepc.offset)

    @classmethod
    def coincidence(cls, query_sepc: QuerySpec, feature_spec: FeatureSpec):
        return chunked.coincidence(query_sepc.path,
                                   processings.coincidence(feature_spec),
                                   query_sepc.limit,
                                   query_sepc.offset)


def load_all(loader, query_spec: QuerySpec, feautre_spec: FeatureSpec):
    offset = query_spec.offset if query_spec.offset is not None else 0
    cache = []
    if query_spec.limit is None:
        if loader == load.photon:
            total = nb.photon(query_spec.path)
        elif loader == load.coincidence:
            total = nb.coincidence(query_spec.path)
        else:
            raise ValueError(
                "Can not auto determin limit for {}.".format(loader))
    else:
        total = query_spec.limit
    while offset < total:
        limit = min(total - offset, query_spec.chunk)
        print('Loading database, {} of {} with chunk {} ...'.format(
            offset, limit, query_spec.chunk))
        cache += loader(query_spec, feautre_spec)
        offset += len(cache)
    return cache
