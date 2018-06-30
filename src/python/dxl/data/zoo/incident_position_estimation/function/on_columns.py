from dxl.data.function import Function, function, OnIterator
from .on_basic import photon2shuffled_hits
from ..data import ShuffledHitsColumns, ShuffledHits, ShuffledCoincidenceHits

__all__ = ['photon_columns2shuffled_hits_columns']


def photon_columns2shuffled_hits_columns(photon_columns, padding_size, shuffle):
    process = OnIterator(photon2shuffled_hits(padding_size, shuffle))
    data = list(process(iter(photon_columns)))
    return ShuffledHitsColumns(ShuffledHits, data)
