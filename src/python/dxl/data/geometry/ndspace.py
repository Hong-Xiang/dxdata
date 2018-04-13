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
        if isinstance(data, Data):
            data = data.d
        if isinstance(data, (list, tuple)):
            data = np.array(data)
        if not isinstance(data, np.ndarray):
            raise TypeError("Unsupported datatype {}.".format(type(data)))
        if data.size != np.max(data.shape):
            raise ValueError("Invalid data shape: {}.".format(data.shape))
        if self.dim is not None and data.size != self.dim:
            fmt = "Invalid data dimension {} when {} is expected for {}."
            raise ValueError(fmt.format(data.size, self.dim, __class__))
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


class GridSpec:
    def __init__(self, start, end, step=None):
        self.start = np.array(start)
        self.end = np.array(end)
        if step is not None:
            self.step = np.array(step)
        else:
            self.step = None

    def spec_of_dim(self, dim: int):
        if self.step is not None:
            return self.start[dim], self.end[dim], self.step[dim]
        else:
            return self.start[dim], self.end[dim]

    def dim(self):
        return self.start.size

    def shape(self):
        result = []
        for i in self.dim():
            s, e, h = self.spec_of_dim(i)
            result.append(int((e - s) / h))
        return result


def grid_index(samples, gird_spec: GridSpec):
    samples = np.array(samples)
    result = np.zeros(samples.shape, np.int32)
    for idim in range(samples.shape[1]):
        start, end, step = gird_spec.spec_of_dim(idim)
        result[:, idim] = (np.floor((samples[:, idim] - start) / step)
                           .astype(np.int32))
    return result


def inbound_mask(samples, grid_spec: GridSpec):
    samples = np.array(samples)
    result = np.empty([samples.shape[0]], bool)
    for i in range(samples.shape[0]):
        result[i] = True
        for j in range(samples.shape[1]):
            start, end, _ = grid_spec.spec_of_dim(j)
            if samples[i, j] < start or samples[i, j] >= end:
                result[i] = False
                break
    return result


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

    def grid_spec(self, start: VectorLowDim, end: VectorLowDim, step: VectorLowDim) -> DataNDArray:
        start = VectorLowDim.from_(start)
        end = VectorLowDim.from_(end)
        step = VectorLowDim.from_(step)
        return GridSpec(start.d, end.d, step.d)

    def histogram_index(self, grid_spec: GridSpec) -> DataNDArray:
        result = grid_index(self.d, gird_spec)
        mask = inbound_mask(self.d, grid_spec)
        return result[mask, :]

    def histogram(self, grid_spec: GridSpec) -> DataNDArray:
        index = self.histogram_index(grid_spec)
        result = np.zeros(grid_spec.shape())
        for i in range(index.shape[0]):
            result[list(index[i, :])] += 1
        return DataNDArray(result)


class PointsWithValue(DataNDArray):
    """
    Points with an extra dims as function dims.
    Thus self.d[:, :pdim] are data for VectorLowDim, and self.d[:, pdim:] are 
    data for function values.
    """

    def __init__(self, point, value=None, dim_point=None):
        """
        Parameters:

        - `point`: DataNDArray or numpy.ndarray, ndarry for points only or 
        combination of point and value. In the latter case, the leading
        `dim_point` columns are treated as point dims.

        - `value`: DataNDArray or numpy.ndarray, if `None`, value will be
        gathered from point.

        - `dim_point`: dimension of point, will be ignored if `value` is provided.
        If `None`, use `point.shape[1] - 1`.
        """
        data = self.convert_data_to_ndarray(point)
        if value is not None:
            value = self.convert_data_to_ndarray(value)
            dim_point = data.shape[1]
            data = np.concatenate([data, value], axis=1)
        super().__init__(data)
        if dim_point is None:
            dim_point = data.shape[1] - 1
            self._squeeze = True
        else:
            self._squeeze = False
        self._dim_point = dim_point

    def dim_point(self):
        return self._point_dim

    def dim_value(self):
        return self.data().shape[1] - self.dim_point()

    def nb_samples(self):
        return self.data().shape[0]

    def histogram(self, grid_spec: GridSpec) -> DataNDArray:
        index = grid_index(self.d[:, :self.dim_point()], gird_spec)
        mask = inbound_mask(self.d[:, :self.dim_point()], grid_spec)
        new_shape = list(grid_spec.shape()) + [1] * self.dim_value()
        result = np.zeros(new_shape)
        for i in range(index.shape[0]):
            if not mask[i]:
                continue
            result[list(index[i, :])] += self.d[i, self.dim_point():]
        return DataNDArray(result)
