from dxl.data.function import Function


class Flatten(Function):
    """

    Relative signatures:

    ## Keras
    ```
    keras.layers.Flatten(data_format=None) :: Optional(str) -> Function
    ```

    `data_format` in Keras implemenation is for keep order when switching dataformat (like NHWC to NCHW) 

    ## TensorFlow
    tf.layers.Flatten(data_format, *args, **kwargs)    
    tf.layers.flatten(inputs)

    ## CNTK
    ```
    cntk.ops.flatten(x, axis=None, name="")
    ```



    """

    def __init__(self, batch_dim=0, shape_hint=None):
        pass

    def __call__(self, x):
        pass


class _Reshape(Function):
    def __init__(self, )
