from ..data import pytable_class, PhotonColumns, CoincidenceColumns, Photon, Coincidence
from functools import singledispatch
from pathlib import Path
from dxl.data.io import PyTableMaker
import numpy as np
from tables import open_file
__all__ = ['columns2pytable']


@singledispatch
def columns2pytable(columns, path_table):
    raise TypeError("Unknown columns type {}.".format(type(columns)))


def insert_photon(row, p: Photon, prefix=''):
    row['{}hits'.format(prefix)] = np.array(
        [[h.x, h.y, h.z, h.e] for h in p.hits])
    if p.hits[0].crystal_index is not None:
        row['{}crystal_index'.format(prefix)] = [
            h.crystal_index for h in p.hits]
    if p.first_hit_index is not None:
        row['{}first_hit_index'.format(prefix)] = p.first_hit_index
    if p.nb_true_hits is not None:
        row['{}nb_true_hits'.format(prefix)] = p.nb_true_hits


def photon_converter(row, p: Photon):
    insert_photon(row, p)
    row.append()


def coincidence_converter(row, c: Coincidence):
    insert_photon(row, c.fst, 'fst/')
    insert_photon(row, c.snd, 'snd/')
    row.append()


@columns2pytable.register(PhotonColumns)
def _(columns: PhotonColumns, path_table: Path):
    maker = PyTableMaker(path_table, pytable_class(columns[0]), )
    return maker.make(iter(columns), photon_converter)


@columns2pytable.register(CoincidenceColumns)
def _(columns: CoincidenceColumns, path_table: Path):
    maker = PyTableMaker(path_table, pytable_class(columns[0]))
    return maker.make(iter(columns), coincidence_converter)
