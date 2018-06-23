from dxl.data.core.function import (Function, function, MultiMethods,
                                    MultiMethodsByTypeOfFirstArg,
                                    MultiMethodsByFirstArg)
import numpy as np
import tensorflow as tf


class TensorMethodsBundle:
    @classmethod
    def implements(cls):
        return {np.ndarray: self._ndarray, tf.Tensor: self._tftensor}

    @classmethod
    def of_type(cls, multi_methods_type, finder=None):
        class NewMultiMethodsFunction(multi_methods_type):
            def __init__(self):
                super().__init__(cls.implements)

        return NewMultiMethodsFunction


TensorMethodsByTypeOfFirstArg = TensorMethodsBundle.of_type(
    MultiMethodsByTypeOfFirstArg)


class _ShapeList(TensorMethodsByTypeOfFirstArg):
    def _ndarray(self, x):
        return list(x.shape)

    def _tftensor(self, x):
        return x.shape.as_list()


shape_list = _ShapeList()


class FullTo(TensorMethodsBundle.of_type(MultiMethodsByFirstArg)):
    @classmethod
    def _ndarray(cls):
        @function
        def FullToNumpy(shape, value, dtype):
            return np.full(shape, value, dtype)

        return FullToNumpy

    @classmethod
    def _tftensor(cls):
        @function
        def FullToTensorFlowConstant(shape, value, dtype):
            return tf.constant(value, tf.as_dtype(dtype), shape, name='Filled')

        return FullToTensorFlowConstant


class _Concatenate(TensorMethodsByTypeOfFirstArg):
    def __call__(self, x, axis=0):
        return super().__call__(x, axis)

    @classmethod
    def _ndarray(cls, x, axis):
        return np.concatenate(x, axis=axis)

    @classmethod
    def _tftensor(cls, x, axis):
        return tf.concat(x, axis)


concatenate = _Concatenate()


class _DType(TensorMethodsByTypeOfFirstArg):
    @classmethod
    def _ndarray(cls, x):
        return x.dtype

    @classmethod
    def _tftensor(cls, x):
        return {
            tf.uint8: np.uint8,
            tf.int32: np.int32,
            tf.float32: np.float32,
            tf.float64: np.float64,
        }[x.dtype]


dtype = _DType


class Padding(Function):
    def __init__(self, size, axis=0, value=None, with_padded_size=False):
        super().__init__()
        self.size = size
        self.axis = axis
        self.value = value
        self.with_padded_size = with_padded_size

    def _pad_size(self, x):
        return self.size - shape_list(x)[self.axis]

    def _pad_shape(self, x):
        if ShapeListOf(x)[self.axis] < size:
            padded_size = size - x.shape[self.axis]

    def _maybe_add_padded_size(self, r, size):
        if self.with_padded_size:
            return r, size
        return r

    def __call__(self, x):
        ps = self._pad_size(x)
        if ps <= 0:
            return self._maybe_add_padded_size(x, ps)
        result = concatenate(
            [x, FullTo(type(x))(ps, self.value, dtype(x))], axis=self.axis)
        return self._maybe_add_padded_size(result, ps)
