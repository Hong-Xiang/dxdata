"""
Convert database to 
"""
from dxl.data.database import session_factory, session_scope
from dxl.data.function import GetAttr, NestMapOf, To, MapByPosition, MapWithUnpackArgsKwargs, Swap, append, Padding, NestMapOf
from tables import IsDescription, Float32Col, UInt32Col
from dxl.data.io import PyTableMaker
from .query import all_photon, all_photon_hits
from .dataclass import ORMTo, HitWithCrystalCenter, Hit, Photon, ShuffledHitsWithIndexAndPaddedSize
import numpy as np
from . import orm
from contextlib import contextmanager


# __all__ = ['hits_class']


@contextmanager
def session(path_db):
    with session_scope(session_factory(path_db)) as sess:
        yield sess


def process(shuffle, padding_size, hit_class):
    return (GetAttr('hits')
            >> NestMapOf(ORMTo(hit_class))
            >> To(Photon)
            >> GetAttr('hits')
            >> shuffle
            >> MapByPosition(0, To(np.array))
            >> MapByPosition(0, Padding(padding_size, is_with_padded_size=True))
            >> MapWithUnpackArgsKwargs(append) >> Swap(1, 2)
            >> MapWithUnpackArgsKwargs(To(ShuffledHitsWithIndexAndPaddedSize)))


def generate_pytable(sess, path_db, hit_dataclass, padding_size, shuffle):
    f = process(shuffle, padding_size, hit_dataclass)

    def it():
        chuck = 100000
        offset = 0
        for i in range(all_photon(sess).count() // chuck):
            photons = all_photon_hits(sess, offset, chuck)
            offset += len(photons)
            if photons is not None:
                for p in photons:
                    yield f(p)
    return it()



dropped = 0


def make_table(path_db, path_table, hit_dataclass, padding_size, shuffle):
    global dropped
    maker = PyTableMaker(
        path_table, pytable_hits_class(padding_size))
    with session(path_db) as sess:
        it = generate_pytable(sess, path_db, hit_dataclass,
                              padding_size, shuffle)

        def converter(row, x):
            global dropped
            if x.hits.shape[0] > padding_size:
                dropped += 1
                return
            for i, k in enumerate(x._fields):
                row[k] = x[i]
            row.append()

        added = maker.make(it, converter)
    print("added {}, dropped {}.".format(added, dropped))
