from abc import ABCMeta, abstractproperty


class WithNamedDim(metaclass=ABCMeta):
    @abstractproperty
    def x(self):
        pass

    @abstractproperty
    def y(self):
        pass

    @abstractproperty
    def z(self):
        pass
