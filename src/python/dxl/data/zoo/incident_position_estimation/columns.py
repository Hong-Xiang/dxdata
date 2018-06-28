from dxl.data.core import ColumnsWithIndex
from .table import pytable_hits_class
from tables import open_file
from .dataclass import ShuffledHitsWithIndexAndPaddedSize
from dxl.data.io import load_npz


class HitsTable(ColumnsWithIndex):
    def __init__(self, path_table, dataclass):
        super().__init__(dataclass)
        self.path = path_table
        self.table = open_file(self.path)

    @property
    def capacity(self):
        pass


class HitsColumnFromNPZ(ColumnsWithIndex):
    def __init__(self, path_npz):
        super().__init__(ShuffledHitsWithIndexAndPaddedSize)
        self.path = path_npz
        self.data = load_npz(self.path)

    @property
    def capacity(self):
        hits = self.data['hits']
        return hits.shape[0] * hits.shape[1]

    def __iter__(self):
        hits = self.data['hits']

        def it():
            for i in range(hits.shape[0]):
                for j in range(hits.shape[1]):
                    d = ShuffledHitsWithIndexAndPaddedSize(
                        self.data['hits'][i, j, ...],
                        self.data['first_hit_index'][i, j],
                        self.data['padded_size'][i, j]
                    )
                    yield d
        return it()

    def __getitem__(self, i):
        return ShuffledHitsWithIndexAndPaddedSize(
            self.data['hits'][i // 32, i % 32, ...],
            self.data['first_hit_index'][i // 32, i % 32],
            self.data['padded_size'][i // 32, i % 32]
        )
