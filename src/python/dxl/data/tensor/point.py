import numpy as np


class Point:
    def __init__(self, data):
        self.data = np.array(data)

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    @property
    def z(self):
        return self.data[2]

    def __eq__(self, p):
        return np.array_equal(self.data, p.data)

    def __repr__(self):
        return f"<Point({self.data})>"

    def __getitem__(self, i):
        return self.data[i]
