from dxl.data.function.tensor import *
import numpy as np
import tensorflow as tf


def test_padding_nparray():
    p = Padding(10)
    x = np.ones([3, 10])
    y = p(x)
    assert y.shape == (10, 10)


def test_padding_list():
    p = Padding(10, 1)
    y = p(np.ones([10, 8]))
    assert y.shape == (10, 10)


def test_shape_list_ndarray():
    x = np.ones([3, 5])
    assert shape_list(x) == [3, 5]


def test_shape_list_tftensor():
    with tf.Graph().as_default() as g:
        x = tf.constant(np.ones([3, 5]))
        assert shape_list(x) == [3, 5]


def test_shape_list_list():
    x = [np.ones([3]), np.ones([3])]
    assert shape_list(x) == [2, 3]


def test_shape_list_not_consist():
    x = [np.ones([3]), np.ones([2])]
    assert shape_list(x) == [2, None]


def test_dtype_np_types():
    assert dtype(np.ones([1], dtype=np.int32)) == np.int32


def test_dtype_tf_types():
    assert dtype(tf.constant([1], dtype=tf.float32)) == np.float32


def test_concatenate_ndarray():
    assert concatenate([np.ones([3]), np.ones([4])]).shape == (7,)


def test_concatenate_list():
    assert concatenate([[1, 2, 3], [3, 4]]) == [1, 2, 3, 3, 4]
