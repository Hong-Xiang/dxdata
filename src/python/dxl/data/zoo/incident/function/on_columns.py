from dxl.data.function import Function, function, OnIterator, Filter
# from .on_basic import photon2shuffled_hits, coincidence2shuffled_hits
# from ..data import (ShuffledHits, ShuffledCoincidenceHits, PhotonColumns, CoincidenceColumns,
# ShuffledHitsColumns)

from ..data import PhotonColumns, CoincidenceColumns

# __all__ = ['raw_columns2shuffled_hits_columns',
#    'filter_by_nb_hits', 'drop_padded_hits']

__all__ = ['FilterPhotonByNbHits', 'FilterCoincidenceByNbHits']


# def _photon_filter(padding_size):
#     def f(p):
#         return len(p.hits) <= padding_size
#     return f


# def _coincidence_filter(padding_size):
#     def f(c):
#         if len(c.photons) != 2:
#             return False
#         return all(map(_photon_filter(padding_size), c.photons))
#     return f


# from functools import singledispatch


# class MapOnColumnsData(Function):
#     def __init__(self, func):
#         self.func = func

#     def __call__(self, columns):
#         return type(columns)(func(columns.data))


# class ShuffleHits(Function):
#     def __init__(self, method):
#         self.method = method

#     def __call__(self, columns):
#         return _shuffle_hits(columns, shuffle)


# @singledispatch
# def _shuffle_hits(c, shuffle):
#     raise TypeError("Unsupported column {}.".format(type(c)))


# @_shuffle_hits.register(PhotonColumns)
# def _(c, shuffle):
#     for h in c.hits:
#         pass

class FilterPhotonByNbHits(Function):
    def __init__(self, nb_hits):
        self.nb_hits = nb_hits

    def __call__(self, columns: PhotonColumns):
        return PhotonColumns([p for p in columns.data
                              if len(p.hits) == self.nb_hits])


class FilterCoincidenceByNbHits(Function):
    def __init__(self, nb_hits, index_of_photon=1):
        self.index_of_photon = index_of_photon
        self.nb_hits = nb_hits

    def __call__(self, columns: CoincidenceColumns):
        return CoincidenceColumns([c for c in columns.data
                                   if len(c.photons[self.index_of_photon].hits) == self.nb_hits])


# def raw_columns2shuffled_hits_columns(raw_columns, padding_size, shuffle):
#     processings = {
#         PhotonColumns: photon2shuffled_hits,
#         CoincidenceColumns: coincidence2shuffled_hits
#     }
#     dataclasses = {
#         PhotonColumns: ShuffledHits,
#         CoincidenceColumns: ShuffledCoincidenceHits}
#     filters = {
#         PhotonColumns: _photon_filter(padding_size),
#         CoincidenceColumns: _coincidence_filter(padding_size)
#     }
#     process = (Filter(filters[type(raw_columns)])
#                >> OnIterator(processings[type(raw_columns)](padding_size, shuffle)))
#     return ShuffledHitsColumns(
#         dataclasses[type(raw_columns)],
#         list(process(raw_columns))
#     )


# def filter_by_nb_hits(source_columns, nb_hits):
#     return ShuffledHitsColumns(
#         source_columns.dataclass,
#         list(Filter(lambda h: h.hits.shape[0] -
#                     h.padded_size == nb_hits)(source_columns))
#     )


# def drop_padded_hits(source_columns, nb_hits):
#     return ShuffledHitsColumns(
#         source_columns.dataclass,
#         list(OnIterator(lambda x: ShuffledHits(x.hits[:nb_hits, :],
#                                                x.first_hit_index,
#                                                x.padded_size))(source_columns.data))
#     )
