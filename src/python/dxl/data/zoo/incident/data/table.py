from tables import IsDescription, Float32Col, UInt32Col
from .basic import Hit, Photon, Coincidence


def pytable_hit_class(padding_size, is_coincidence):
    if is_coincidence:
        nb_features = 8
    else:
        nb_features = 4

    class Hits(IsDescription):
        hits = Float32Col([padding_size, nb_features])
        first_hit_index = UInt32Col()
        padded_size = UInt32Col()
    return Hits


from functools import singledispatch


@singledispatch
def pytable_class(obj):
    raise TypeError("Unknown type {}.".format(type(obj)))


@pytable_class.register(Photon)
def _(obj):
    h = obj.hits[0]
    if h.crystal_index is not None:
        class Hits(IsDescription):
            hits = Float32Col([h.padded_size, 4])
            crystal_index = UInt32Col()
            first_hit_index = UInt32Col()
            padded_size = UInt32Col()
