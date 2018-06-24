from dxl.data.core.function import (Function, function, MultiMethodsFunction,
                                    MultiMethodsByTypeOfFirstArg,
                                    MultiMethodsByFirstArg,
                                    head)
import numpy as np
import tensorflow as tf

__all__ = ['shape_list', 'FullTo', 'concatenate', 'dtype', 'Padding']


class TensorMethodsBundle:
    def implements(self):
        return {np.ndarray: self._impl_ndarray,
                tf.Tensor: self._impl_tftensor,
                list: self._impl_iter,
                tuple: self._impl_iter, }

    @classmethod
    def of_type(cls, multi_methods_type):
        class NewMultiMethodsFunction(multi_methods_type, TensorMethodsBundle):
            def __init__(self):
                super().__init__(self.implements())

        return NewMultiMethodsFunction

    @classmethod
    def of_finder(cls, finder):
        class NewMultiMethodsFunction(MultiMethodsFunction, TensorMethodsBundle):
            def __init__(self):
                super().__init__(self.implements(), finder)

        return NewMultiMethodsFunction


TensorMethodsByTypeOfFirstArg = TensorMethodsBundle.of_type(
    MultiMethodsByTypeOfFirstArg)


class _ShapeList(TensorMethodsByTypeOfFirstArg):
    def _impl_ndarray(self, x):
        return list(x.shape)

    def _impl_tftensor(self, x):
        return x.shape.as_list()

    def _impl_iter(self, x):
        shapes = [shape_list(_) for _ in x]
        dims = set(len(s) for s in shapes)
        if not len(dims) == 1:
            raise ValueError(
                "Not all data in same dimension, dims {}.".format(dims))
        ndim = int(dims.pop())
        shapes_t = [set(s[i] for s in shapes) for i in range(ndim)]
        return [len(x)] + [s.pop() if len(s) == 1 else None for s in shapes_t]


shape_list = _ShapeList()


class FullTo(TensorMethodsBundle, MultiMethodsFunction):
    def _finder_impl(self, *args, **kwargs):
        return self.target_type

    def __init__(self, target_type):
        super().__init__(self.implements(), finder=self._finder_impl)
        self.target_type = target_type

    @classmethod
    def _impl_ndarray(cls, shape, value, dtype):
        return np.full(shape, value, dtype)

    @classmethod
    def _impl_tftensor(cls, shape, value, dtype):
        return tf.constant(value, tf.as_dtype(dtype), shape, name='Filled')

    @classmethod
    def _impl_iter(cls, shape, value, dtype):
        raise NotImplementedError(
            "No implementation for FullTo to list or tuple")


class _Concatenate(TensorMethodsBundle.of_finder(lambda x, axis: type(head(x)))):
    def __call__(self, x, axis=0):
        return super().__call__(x, axis)

    @classmethod
    def _impl_ndarray(cls, x, axis):
        return np.concatenate(x, axis=axis)

    @classmethod
    def _impl_tftensor(cls, x, axis):
        return tf.concat(x, axis)

    @classmethod
    def _impl_iter(cls, x, axis):
        if axis != 0:
            raise NotImplementedError(
                "concatenate of list or tuple with axis != 0 is not implemented yet.")
        import itertools
        return [_ for _ in itertools.chain(*x)]


concatenate = _Concatenate()


class _DType(TensorMethodsByTypeOfFirstArg):
    @classmethod
    def _impl_ndarray(cls, x):
        return x.dtype

    @classmethod
    def _impl_tftensor(cls, x):
        return {
            tf.uint8: np.uint8,
            tf.int32: np.int32,
            tf.float32: np.float32,
            tf.float64: np.float64,
        }[x.dtype]

    @classmethod
    def _impl_iter(cls, x):
        raise NotImplementedError(
            "_DType for list or tuple is not implemented yet.")


dtype = _DType()


class Padding(Function):
    def __init__(self, size, axis=0, value=0.0, is_with_padded_size=False):
        super().__init__()
        self.size = size
        self.axis = axis
        self.value = value
        self.is_with_padded_size = is_with_padded_size

    def _pad_size(self, x):
        return self.size - shape_list(x)[self.axis]

    def _pad_shape(self, x):
        result = shape_list(x)
        result[self.axis] = self._pad_size(x)
        return result

    def _maybe_add_padded_size(self, r, size):
        if self.is_with_padded_size:
            return r, size
        return r

    def __call__(self, x):
        ps = self._pad_size(x)
        if ps <= 0:
            return self._maybe_add_padded_size(x, ps)
        result = concatenate(
            [x, FullTo(type(x))(self._pad_shape(x), self.value, dtype(x))],
            axis=self.axis)
        return self._maybe_add_padded_size(result, ps)
