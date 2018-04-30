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
            else:
                raise ValueError("Batchdim != 0 is not implemented yet.")
            print('Not using compression')
            h5group.create_dataset(
                k,
                data=dct_of_ndarray[k],
                shape=dct_of_ndarray[k].shape,
                dtype=dct_of_ndarray[k].dtype,
                chunks=tuple(chunk_size),
            # )

            compression="gzip")
            # compression="gzip")


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
