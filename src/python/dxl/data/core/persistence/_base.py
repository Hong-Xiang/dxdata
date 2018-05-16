class PersistentData:
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path


class PersistentDataInDataset(PersistentData):
    def __init__(self, path_file, path_dataset):
        super().__init__(path_file)
        self._path_dataset = path_dataset

    @property
    def path_dataset(self):
        return self._path_dataset
