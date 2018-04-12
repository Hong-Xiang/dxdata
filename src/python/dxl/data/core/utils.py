from functools import wraps


def unbox(**kwargs):
  for name, type_ in kwargs.values():
    pass

  def warpper(func):
    def call(*args, **kwargs):
      func(*args, **kwargs)

    return call

  return warpper