from .data import Coincidence, Photon, Hit
from tables import open_file

from dxl.data.utils import logger
import numpy as np

__all__ = ['load_table']


def _photon_loader(row: np.void) -> Photon:
    if 'crystal_index' in row.dtype.fields:
        hits = [Hit(*h, ci)
                for h, ci in zip(row['hits'], row['crystal_index'])]
    else:
        hits = [Hit(*h) for h in row['hits']]
    nb_true_hits = row['nb_true_hits'] if 'nb_true_hits' in row.dtype.fields else None
    first_hit_index = row['first_hit_index'] if 'first_hit_index' in row.dtype.fields else None
    return Photon(hits, first_hit_index, nb_true_hits)


def _coincidence_loader(row) -> Coincidence:
    return Coincidence(list(map(_photon_loader, [row['fst'], row['snd']])))


def _get_loader(table):
    if isinstance(table, np.ndarray):
        if 'fst' in table.dtype.fields:
            return _coincidence_loader
        else:
            return _photon_loader
    if table.colnames == ['fst', 'snd']:
        return _coincidence_loader
    else:
        return _photon_loader


@logger.before.info('Loading pytable data')
def load_table(path, limit=None):
    with open_file(path) as fin:
        table = fin.root.data
        loader = _get_loader(table)
        if limit is None:
            limit = table.nrows
        return [loader(table[i]) for i in range(limit)]
