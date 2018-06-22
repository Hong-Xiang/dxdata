from dxl.learn.dataset import DataColumns
from dxl.data.database import get_or_create_session
import tqdm
import numpy as np
from .query import nb_photon, all_photon
from contextlib import contextmanager
import random

dataset_path = '../../../data/gamma.db'


class PhotonDataColumns(DataColumns):
    def _process(self, data):
        if isinstance(data, str):
            path = data
            is_shuffle = True
        else:
            path = data['path']
            is_shuffle = data['is_shuffle']
        self.data = get_or_create_session(path)
        self.is_shuffle = is_shuffle

    @property
    def columns(self):
        return tuple(['hits', 'first_hit'])

    def _calculate_capacity(self):
        return nb_photon()

    def _make_iterator(self):
        def it():
            for p in all_photon():
                hits = [h.to_list() for h in p.hits]
                random.shuffle(hits)
                first_hit = None
                for i, h in enumerate(hits):
                    if h[4] == 0:
                        first_hit = i
                        break
                if first_hit is None:
                    raise TypeError(
                        "First hit is not found in {}.".format(hits))
                hits = np.array(hits)[:, :4]
                yield {'hits': hits, 'first_hit': first_hit}

        return it()