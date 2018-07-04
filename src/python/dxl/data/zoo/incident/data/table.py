from tables import IsDescription, Float32Col, UInt32Col
from . import basic


# def pytable_hit_class(padding_size, is_coincidence):
#     if is_coincidence:
#         nb_features = 8
#     else:
#         nb_features = 4

#     class Hits(IsDescription):
#         hits = Float32Col([padding_size, nb_features])
#         first_hit_index = UInt32Col()
#         padded_size = UInt32Col()
#     return Hits

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
                crystal_index = UInt32Col()
                first_hit_index = UInt32Col()
                nb_true_hits = UInt32Col()
            return Photon
        else:
            class Photon(IsDescription):
                hits = Float32Col([len(template.hits), 4])
                crystal_index = UInt32Col()
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
        photon0 = pytable_class(template.photons[0])
        photon1 = pytable_class(template.photons[1])
    return Coincidence
