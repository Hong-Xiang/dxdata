from dxl.data import ColumnsWithIndex
from .basic import Photon, Hit, Coincidence
from .processed import ShuffledHits, ShuffledCoincidenceHits
from ..database import nb, chunked
from dxl.data.core import ColumnsWithIndex
from tables import open_file
from dxl.data.io import load_npz
from tqdm import tqdm

__all__ = ['PhotonColumns', 'CoincidenceColumns']


class ColumnsWithIndexInMemory(ColumnsWithIndex):
    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, i):
        return self.data[i]


class RawDataColumns(ColumnsWithIndexInMemory):
    def __init__(self, dataclass, path, is_crystal_center, limit, chunk=None):
        super().__init__(dataclass)
        self.path = path
        self.limit = limit
        self.is_crystal_center = is_crystal_center
        self.chunk = chunk or 100000
        self.data = None
        self.data = self.load_data()

    def load_data(self):
        offset = 0
        cache = []
        if self.limit is None:
            limit = self.raw_data_capacity()
        else:
            limit = self.limit
        while offset < limit:
            limit_ = min(limit - offset, self.chunk)
            print('Loading database, {} of {} with chunk {} ...'.format(
                offset, limit, self.chunk))
            cache += self.load_chunk(offset, limit_)
            offset = len(cache)
        return cache

    @property
    def capacity(self):
        if self.data is None:
            return self.get_capacity()
        return len(self.data)


class PhotonColumns(RawDataColumns):
    def __init__(self, path, is_crystal_center=True, limit=None, chunk=None):
        super().__init__(Photon, path, is_crystal_center, limit, chunk)

    def load_chunk(self, offset, limit):
        from ..function import processings
        return chunked.photon(self.path, processings.photon(self.is_crystal_center), limit, offset)

    def raw_data_capacity(self):
        from ..database import nb
        return nb.photon(self.path)


class CoincidenceColumns(RawDataColumns):
    def __init__(self, path, is_crystal_center=True, limit=None, chunk=None):
        super().__init__(Coincidence, path, is_crystal_center, limit, chunk)

    def load_chunk(self, offset, limit):
        from ..function import processings
        return chunked.coincidence(self.path, processings.coincidence(self.is_crystal_center), limit, offset)

    def raw_data_capacity(self):
        from ..database import nb
        return nb.coincidence(self.path)


class ShuffledHitsColumns(ColumnsWithIndexInMemory):
    def __init__(self, dataclass, data):
        super().__init__(dataclass)
        self.data = data

    @property
    def capacity(self):
        return len(self.data)


class ShuffledHitsTable(ColumnsWithIndexInMemory):
    def __init__(self, path_table):
        self.path = path_table
        self.file = open_file(self.path)
        self.table = self.file.root.data
        super().__init__(self.get_dataclass())
        self.data = self.load_all()
        self.file.close()

    def get_dataclass(self):
        if self.table[0]['hits'].shape[1] == 4:
            return ShuffledHits
        elif self.table[0]['hits'].shape[1] == 8:
            return ShuffledCoincidenceHits
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


__all__ += ['ShuffledHitsColumns', 'ShuffledHitsTable']

# class ShuffledHitsNPZColumns(ColumnsWithIndex):
#     def __init__(self, path_npz):
#         super().__init__(ShuffledHitsWithIndexAndPaddedSize)
#         self.path = path_npz
#         self.data = load_npz(self.path)

#     @property
#     def capacity(self):
#         hits = self.data['hits']
#         return hits.shape[0] * hits.shape[1]

#     def __iter__(self):
#         hits = self.data['hits']

#         def it():
#             for i in range(hits.shape[0]):
#                 for j in range(hits.shape[1]):
#                     d = ShuffledHitsWithIndexAndPaddedSize(
#                         self.data['hits'][i, j, ...],
#                         self.data['first_hit_index'][i, j],
#                         self.data['padded_size'][i, j]
#                     )
#                     yield d
#         return it()

#     def __getitem__(self, i):
#         return ShuffledHitsWithIndexAndPaddedSize(
#             self.data['hits'][i // 32, i % 32, ...],
#             self.data['first_hit_index'][i // 32, i % 32],
#             self.data['padded_size'][i // 32, i % 32]
#         )
