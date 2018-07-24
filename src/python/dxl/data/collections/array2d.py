"""
Helper class for 2D array
"""


class Array2D:
    def __init__(self, data, nb_rows, nb_columns=None):
        self.data = data

    def __getitem__(self, i):
        return self.data[i[0]][i[1]]
