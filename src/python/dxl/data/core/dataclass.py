class DataClass:
    """
    Dataclass mixin.
    Requires: __slots__
    """

    def __init__(self, *args, **kwargs):
        found = []
        for n, v in zip(self.__slots__, args):
            setattr(self, n, v)
            found.append(n)
        for k, v in kwargs.items():
            if self.__slots__.index(k) < len(args):
                raise TypeError(
                    f"{self.__init__} got multiple values for argument {k}")
            setattr(self, k, v)
            found.append(k)
        if len(found) < len(self.__slots__):
            raise TypeError(f"TypeError: {type(self)} missing {len(__slots__) - len(found)}"
                            f" required positional arguments: {[n for n in self.__slots__ if not n in found]}")

    def replace(self, **kwargs):
        for k in self.__slots__:
            if not k in kwargs:
                kwargs[k] = getattr(self, k)
        return type(self)(**kwargs)

    def __repr__(self):
        class_name = type(self).__name__
        inner = {k: getattr(self, k) for k in self.__slots__}
        return f"{class_name}({inner})"

    def __eq__(self, others) -> bool:
        return all(getattr(self, k) == getattr(others, k) for k in self.__slots__)

    def __hash__(self):
        return hash(tuple(map(getattr(self, self.__slots__))))

    @classmethod
    def fields(cls):
        return tuple(cls.__slots__)

    def asdict(self):
        return {k: getattr(self, k) for k in self.fields()}

    def astuple(self):
        return tuple((getattr(self, k) for k in self.fields))
