from dxl.data.function import Function, function, OnIterator, Filter
from .on_basic import photon2shuffled_hits, coincidence2shuffled_hits
from ..data import (ShuffledHits, ShuffledCoincidenceHits, PhotonColumns, CoincidenceColumns,
                    ShuffledHitsColumns)

__all__ = ['raw_columns2shuffled_hits_columns',
           'filter_by_nb_hits', 'drop_padded_hits']


def _photon_filter(padding_size):
    def f(p):
        return len(p.hits) <= padding_size
    return f


def _coincidence_filter(padding_size):
    def f(c):
        if len(c.photons) != 2:
            return False
        return all(map(_photon_filter(padding_size), c.photons))
    return f


def raw_columns2shuffled_hits_columns(raw_columns, padding_size, shuffle):
    processings = {
        PhotonColumns: photon2shuffled_hits,
        CoincidenceColumns: coincidence2shuffled_hits
    }
    dataclasses = {
        PhotonColumns: ShuffledHits,
        CoincidenceColumns: ShuffledCoincidenceHits}
    filters = {
        PhotonColumns: _photon_filter(padding_size),
        CoincidenceColumns: _coincidence_filter(padding_size)
    }
    process = (Filter(filters[type(raw_columns)])
               >> OnIterator(processings[type(raw_columns)](padding_size, shuffle)))
    return ShuffledHitsColumns(
        dataclasses[type(raw_columns)],
        list(process(raw_columns))
    )


def filter_by_nb_hits(source_columns, nb_hits):
    return ShuffledHitsColumns(
        source_columns.dataclass,
        list(Filter(lambda h: h.hits.shape[0] -
                    h.padded_size == nb_hits)(source_columns))
    )


def drop_padded_hits(source_columns, nb_hits):
    return ShuffledHitsColumns(
        source_columns.dataclass,
        list(OnIterator(lambda x: ShuffledHits(x.hits[:nb_hits, :],
                                               x.first_hit_index,
                                               x.padded_size))(source_columns.data))
    )

# def photon_columns2shuffled_hits_columns(photon_columns, padding_size, shuffle):
#     process = OnIterator(photon2shuffled_hits(padding_size, shuffle))
#     data = list(process(iter(photon_columns)))
#     return ShuffledHitsColumns(ShuffledHits, data)


# def coincidence_columns2shuffled_hits_columns(coincidence_columns, padding_size, shuffle):
#     prosses = OnIterator()
