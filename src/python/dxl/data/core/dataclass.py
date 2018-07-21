class DataClass:
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
        result = True
        result = ((result and (getattr(self, k) == getattr(others, k)))
                  for k in self.__slots__)
        return result

    def __hash__(self):
        return hash(tuple(map(getattr(self, self.__slots__))))

    @classmethod 
    def fields(cls):
        return tuple(cls.__slots__)