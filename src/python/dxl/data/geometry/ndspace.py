from ..core import Data, DataNDArray, DataIterable
import numpy as np


class VectorLowDim(Data):

    dim = None

    def __init__(self, data):
        """
        Parameters:

        - `data`: VectorLowDim, list/tuple or numpy.ndarray of correspongding dimension.

        Raises:

        - `TypeError` if given data with unsupported type.
        - `ValueError` if given data with invalid dimension.
        """
        if isinstance(data, VectorLowDim):
            data = data.d
        if isinstance(data, (list, tuple)):
            data = np.array(data)
        if not isinstance(data, np.ndarray):
            raise TypeError("Unsupported datatype {}.".format(type(data)))
        if self.dim is not None and data.dim != self.dim:
            fmt = "Invalid data dimension {} when {} is expected for {}."
            raise ValueError(fmt.format(data.ndim, self.dim, __class__))
        super().__init__(np.array(data))


class Vector1(VectorLowDim):
    dim = 1

    def x(self):
        return Data(self.d[0])


class Vector2(VectorLowDim):
    dim = 2

    def x(self):
        return Data(self.d[0])

    def y(self):
        return Data(self.d[1])


class Vector3(VectorLowDim):
    dim = 3

    def x(self):
        return Data(self.d[0])

    def y(self):
        return Data(self.d[1])

    def z(self):
        return Data(self.d[2])


class Points(DataNDArray):
    """
    Data of VectorLowDim.
    """

    def __init__(self, data):
        super().__init__(data)
        if self.dim() > 3 or self.dim() < 1:
            raise ValueError("Invalid data shape {}.".format(self.d.shape))

    def nb_samples(self):
        return self.d.shape[0]

    def dim(self):
        return self.d.shape[1]

    def to_list(self) -> DataIterable:
        cls = [None, Vector1, Vector2, Vector3][self.dim()]
        return DataIterable([cls(self.d[i, ...]) for i in range(self.nb_samples())])

    def histogram(self, start: VectorLowDim, end: VectorLowDim, step: VectorLowDim) -> DataNDArray:
        start = VectorLowDim.from_(start)
        end = VectorLowDim.from_(end)
        step = VectorLowDim.from_(step)

        def grid_index():
            result = np.zeros(self.data().shape, np.int32)
            for idim in range(self.dim()):
                _start, _end, _step = start.d[idim], end.d[idim], step.d[idim]
                result[:, idim] = (np.floor((self.data()[:, idim] - _start) / _step)
                                   .astype(np.int32))
            return result

        def drop_outbound(index):
            mask = np.empty([index.shape[0]], bool)
            for i in range(index.shape[0]):
                mask[i] = True
                for j in range(self.dim()):
                    if self.d[i, j] < start.d[j] or self.d[i, j] >= end.d[j]:
                        mask[i] = False
                        break
            return index[mask, :]
        return DataNDArray(drop_outbound(grid_index()))
