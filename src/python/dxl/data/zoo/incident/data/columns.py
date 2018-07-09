from dxl.data import ColumnsWithIndex
from .spec import FeatureSpec
from .basic import Photon, Hit, Coincidence
from .processed import ShuffledHits, ShuffledCoincidenceHits
from ..database import nb, chunked
from dxl.data.core import ColumnsWithIndex
from tables import open_file
from dxl.data.io import load_npz
from tqdm import tqdm

__all__ = ['PhotonColumns', 'CoincidenceColumns']


class ColumnsWithIndexInMemory(ColumnsWithIndex):
    def __init__(self, dataclass, data):
        super().__init__(dataclass)
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, i):
        return self.data[i]

    @property
    def capacity(self):
        return len(self.data)


class PhotonColumns(ColumnsWithIndexInMemory):
    def __init__(self, data):
        super().__init__(Photon, data)


class CoincidenceColumns(ColumnsWithIndexInMemory):
    def __init__(self, data):
        super().__init__(Coincidence, data)


class ShuffledHitsTable(ColumnsWithIndexInMemory):
    def __init__(self, path_table):
        self.path = path_table
        self.file = open_file(self.path)
        self.table = self.file.root.data
        super().__init__(self.get_dataclass())
        self.data = self.load_all()
        self.file.close()

    def get_dataclass(self):
        if self.table.columns['hits'].shape[1] == 4:
            return Photon
        elif self.table[0]['hits'].shape[1] == 8:
            return Coincidence
        raise ValueError()

    def load_all(self):
        print('Loading data...')
        keys = ['hits', 'first_hit_index', 'padded_size']
        cache = {}
        for k in keys:
            cache[k] = self.table[:][k]
        data = [self.dataclass(*(cache[k][i] for k in keys))
                for i in range(cache['hits'].shape[0])]
        return data

    @property
    def capacity(self):
        return len(self.data)

    @property
    def padding_size(self):
        return self.data[0].hits.shape[0]

    def close(self):
        self.file.close()


__all__ += ['ShuffledHitsTable']
