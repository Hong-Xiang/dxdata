from .data import Data
import dask


class DataFrame(Data):
    pass


class DataIterableDask(Data):
    def map(self, func) -> 'DataIterableDask':
        return DataIterableDask(dask.delayed(map)(func, self.data()))


class DataIterableWithUnknownKeys(Data):
    def select(self, key):
        return DataFrame(self.d.get_group(key))

    def drop_keys(self) -> ResultsDask:
        return self.map(lambda x: x[1])
