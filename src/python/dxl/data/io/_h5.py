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
    if batch_dim == 0:
      chunk_size = tuple([1] + list(dct_of_ndarray[k].shape[1:]))
    else:
      raise ValueError("Batchdim != 0 is not implemented yet.")
    h5group.create_dataset(
        k,
        data=dct_of_ndarray[k],
        shape=dct_of_ndarray[k].shape,
        dtype=dct_of_ndarray[k].dtype,
        chunks=tuple(chunk_size),
        compression="gzip")
