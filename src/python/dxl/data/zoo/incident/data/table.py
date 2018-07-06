from tables import IsDescription, Float32Col, UInt32Col
from . import basic

__all__ = ['pytable_class']

from functools import singledispatch


@singledispatch
def pytable_class(template):
    raise TypeError("Unknown type {}.".format(type(obj)))


@pytable_class.register(basic.Photon)
def _(template):
    h = template.hits[0]
    if h.crystal_index is not None:
        if template.first_hit_index is not None:
            class Photon(IsDescription):
                hits = Float32Col([len(template.hits), 4])
                crystal_index = UInt32Col([len(template.hits)])
                first_hit_index = UInt32Col()
                nb_true_hits = UInt32Col()
            return Photon
        else:
            class Photon(IsDescription):
                hits = Float32Col([len(template.hits), 4])
                crystal_index = UInt32Col([len(template.hits)])
            return Photon
    else:
        if template.first_hit_index is not None:
            class Photon(IsDescription):
                hits = Float32Col([len(template.hits), 4])
                first_hit_index = UInt32Col()
                nb_true_hits = UInt32Col()
            return Photon
        else:
            class Photon(IsDescription):
                hits = Float32Col([len(template.hits), 4])
            return Photon


@pytable_class.register(basic.Coincidence)
def _(template: basic.Coincidence):
    class Coincidence(IsDescription):
        fst = pytable_class(template.fst)
        snd = pytable_class(template.snd)
    return Coincidence
