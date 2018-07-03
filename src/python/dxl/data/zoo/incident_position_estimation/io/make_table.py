"""
Convert database to 
"""
from dxl.data.database import session_factory, session_scope
from dxl.data.function import GetAttr, NestMapOf, To, MapByPosition, MapWithUnpackArgsKwargs, Swap, append, Padding, NestMapOf
from dxl.data.io import PyTableMaker
from contextlib import contextmanager
from ..data import pytable_hit_class, PhotonColumns, CoincidenceColumns
from ..function import sort_hits_by_energy, raw_columns2shuffled_hits_columns


def make_table(path_db, path_table, is_crystal_center, is_coincidence, padding_size, shuffle, limit=None, chunk=None):
    maker = PyTableMaker(path_table, pytable_hit_class(
        padding_size, is_coincidence))
    if is_coincidence:
        columns_class = CoincidenceColumns
    else:
        columns_class = PhotonColumns
    columns = columns_class(path_db, is_crystal_center, limit, chunk)
    shuffled_hits_columns = raw_columns2shuffled_hits_columns(
        columns, padding_size, shuffle)
    added = maker.make(iter(shuffled_hits_columns))
    return added
