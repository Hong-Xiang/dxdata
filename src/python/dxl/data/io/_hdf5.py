from typing import Dict
import numpy as np
import h5py


def h5_add_dataset(h5group, dct_of_ndarray, batch_dim=0, tqdm=None):
    """
    Add dict of numpy ndarray to hdf5 group/file.

    :param batch_dim: dimension which is expanded when calculating chunks,
                        e.g. for a ndarray with shape `[10, 5, 5, 1]`, and `batch_dim = 0`,
                        the chunks will be `[1, 5, 5, 1]`.
    """
    if tqdm is None:
        to_iter = dct_of_ndarray
    else:
        to_iter = tqdm(dct_of_ndarray, leave=False)
    for k in to_iter:
        print('Saving', k)
        if isinstance(dct_of_ndarray[k], dict):
            g = h5group.create_group(k)
            h5_add_dataset(g, dct_of_ndarray[k], batch_dim, tqdm)
        else:
            if batch_dim == 0:
                chunk_size = [1] + list(dct_of_ndarray[k].shape[1:])
                nb_chunks = dct_of_ndarray[k].shape[0] // chunk_size[0]
                # Fix for h5py memory leak
                if nb_chunks > 10000:
                    chunk_size[0] = dct_of_ndarray[k].shape[0] // 10000
                chunk_size = tuple(chunk_size)
                if dct_of_ndarray[k].shape[0] == 0:
                    chunk_size = None
            else:
                raise ValueError("Batchdim != 0 is not implemented yet.")
            h5group.create_dataset(
                k,
                data=dct_of_ndarray[k],
                shape=dct_of_ndarray[k].shape,
                dtype=dct_of_ndarray[k].dtype,
                chunks=chunk_size,
                compression="gzip")


def save_h5(file_path,
            dataset: Dict[str, np.ndarray],
            dataset_path=None,
            *,
            tqdm=None):
    """
    Save dict of ndarray to hdf5 file.

    - `file_path` path of hdf5 file in filesystem.
    - `dataset` dict of np.ndarray to be saved.
    - `dataset_path` in file group path, if is `None`, `'/'` will be used.
    - `tqdm` progress bar to be used
    """
    dataset_path = dataset_path or '/'
    with h5py.File(file_path) as fout:
        g = fout.require_group(dataset_path)
        h5_add_dataset(g, dataset, tqdm=tqdm)


def load_h5(path_file, path_dataset=None, slices=None):
    """
    Load numpy.ndarray from HDF5 file.
    
    Args:
    - `path_file`: `str` or `pathlib.Path`, path of hdf5 file
    - `path_dataset`: dataset path in file 
    - `slices`: tuple of slice objects or `None`, or str
    """
    if isinstance(slices, str):
        from ..utils.slices import slices_from_str
        slices = slices_from_str(slices)
    if path_dataset is None:
        path_dataset = '/'
    with h5py.File(path_file, 'r') as fin:
        if slices is None:
            return np.array(fin[path_dataset])
        else:
            return np.array(fin[path_dataset][slices])