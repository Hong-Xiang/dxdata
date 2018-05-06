import numpy as np


def assert_dimension(data, required_dimension, name=None, msg=None):
    """
    Perform two checks:
    1. data must have .ndim attribute;
    2. data.ndim must return value of `required_dimension`;
    Otherwise raises ValueError.

    Name is subsititude in standard output message.
    if msg is not None, msg is returned with msg.format(name=name, required_dimension=required_dimension, got_dimension=data.ndim)
    """
    if data.ndim != required_dimension:
        if msg is None:
            msg = "{name} dimension is required to be {required_dimension}, however got {got_dimension}."
            raise ValueError(
                msg.format(
                    name=name,
                    required_dimension=required_dimension,
                    got_dimension=data.ndim))
