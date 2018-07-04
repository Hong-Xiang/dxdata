from ..data import pytable_class, PhotonColumns, CoincidenceColumns, Photon, Coincidence
from functools import singledispatch
from pathlib import Path
from dxl.data.io import PyTableMaker
import numpy as np

__all__ = ['columns2pytable']

@singledispatch
def columns2pytable(columns, path_table):
    raise TypeError("Unknown columns type {}.".format(type(columns)))

def photon_converter(row, p:Photon):
    row['hits'] = np.array([[h.x, h.y, h.z, h.e] for h in p.hits])
    if p.first_hit_index is not None:
        row['first_hit_index'] = p.first_hit_index
    if p.nb_true_hits is not None:
        row['nb_true_hits'] = p.nb_true_hits
    row.append()

@columns2pytable.register(PhotonColumns)
def _(columns: PhotonColumns, path_table: Path):
    maker = PyTableMaker(path_table, pytable_class(columns[0]), )
    return maker.make(iter(columns), photon_converter)
    
@columns2pytable.register(CoincidenceColumns)
def _(columns: CoincidenceColumns, path_table: Path):
    maker = PyTableMaker(path_table, pytable_class(columns[0]))
    return maker.make(iter(columns))
 
