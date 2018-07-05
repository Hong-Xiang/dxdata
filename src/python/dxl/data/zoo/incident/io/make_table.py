"""
Convert database to 
"""
from dxl.data.function import GetAttr, NestMapOf, To, MapByPosition, MapWithUnpackArgsKwargs, Swap, append, Padding, NestMapOf
from dxl.data.io import PyTableMaker
from contextlib import contextmanager
from ..data import PhotonColumns, CoincidenceColumns, QuerySpec, FeatureSpec
from ..function import database_load_all, database_loader, columns2pytable


def db2table(path_table, query_spec:QuerySpec, feature_spec:FeatureSpec, processing=None):
    loader = {
        'photon': database_loader.photon,
        'coincidence': database_loader.coincidence
    }[feature_spec.main_feature]
    data = database_load_all(loader, query_spec, feature_spec)
    columns = {
        'photon': PhotonColumns,
        'coincidence': CoincidenceColumns,
    }[feature_spec.main_feature](data)
    if processing is not None:
        columns = processing(columns)
    return columns2pytable(columns, path_table)

    # maker = PyTableMaker(path_table, pytable_hit_class(
    #     padding_size, is_coincidence))
    # if is_coincidence:
    #     columns_class = CoincidenceColumns
    # else:
    #     columns_class = PhotonColumns
    # columns = columns_class(path_db, is_crystal_center, limit, chunk)
    # shuffled_hits_columns = raw_columns2shuffled_hits_columns(
    #     columns, padding_size, shuffle)
    # added = maker.make(iter(shuffled_hits_columns))
    # return added
