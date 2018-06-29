from dxl.data import ColumnsWithIndex
from .basic import Photon
from ..database.query import nb
from dxl.data.core import ColumnsWithIndex
from .table import pytable_hits_class
from tables import open_file
from .dataclass import ShuffledHitsWithIndexAndPaddedSize
from dxl.data.io import load_npz
from tqdm import tqdm


class RawDataColumns(ColumnsWithIndex):
    def __init__(self, dataclass, path, is_load_all=True, chunk=None):
        super().__init__(dataclass)
        self.path = path
        self.cache = None
        self.chunk = chunk

    def __getitem__(self, i):
        if self.cache is None or len(self.cache) < i:
            self.cache = self.load_data(i)

    def __iter__(self):
        if self.cache is None:
            self.cache = self.load_data()
        return iter(self.cache)


class PhotonColumns(RawDataColumns):
    def __init__(self, path, hit_dataclass, is_load_all=True, chunk=100000):
        super().__init__(Photon, path, is_load_all, chunk)
        self.hit_dataclass = hit_dataclass

    @property
    def capacity(self):
        if self.cache is None:
            return nb.photon(self.path)
        else:
            return len(self.cache)

    def _make_db_scanner(self):
        process = NestMapOf((GetAttr('hits')
                             >> NestMapOf(ORMTo(self.hit_dataclass))
                             >> To(Photon)))
        query = {
            Hit: chunked_photon_hits,
            HitWithCrystalCenter: chunked_photon_hits_with_crystals
        }[self.hit_dataclass]
        return ChunkedDBScannerWith(self.path,
                                    function(query) >> process,
                                    self.chunk)

    @property
    def dtypes(self):
        return {'hits': self.hit_dataclass}


class CoincidenceColumns(ColumnsWithIndex):
    def __init__(self, path, hit_dataclass, is_load_all=True, chunk=10000):
        ...


class ShuffledHitsColumns(Columns):
    def __init__(self, source_columns: Columns, dataclass, processing):
        super().__init__(dataclass)
        self.source_columns = source_columns
        self.processing = processing

    @property
    def capacity(self):
        return self.source_columns.capacity

    def __iter__(self):
        return self.processing(self.source_columns)


class HitsTable(ColumnsWithIndex):
    def __init__(self, path_table):
        super().__init__(ShuffledHitsWithIndexAndPaddedSize)
        self.path = path_table
        self.file = open_file(self.path)
        self.table = self.file.root.photon_hits.simluated
        self.cache = None
        self.load_all()

    def load_all(self):
        print('Loading data...')
        self.cache = {}
        for k in ['hits', 'first_hit_index', 'padded_size']:
            self.cache[k] = self.table[:][k]

    @property
    def capacity(self):
        return self.table.shape[0]

    @property
    def padding_size(self):
        return self.table[0]['hits'].shape[0]

    def load_data(self, i):
        if self.cache is None:
            return self.dataclass(self.table[i]['hits'],
                                  self.table[i]['first_hit_index'],
                                  self.table[i]['padded_size'])
        else:
            return self.dataclass(self.cache['hits'][i, ...],
                                  self.cache['first_hit_index'][i],
                                  self.cache['padded_size'][i])

    def __getitem__(self, i):
        return self.load_data(i)

    def close(self):
        self.file.close()


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
