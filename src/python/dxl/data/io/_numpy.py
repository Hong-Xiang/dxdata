from pathlib import Path
from dxl.core.log import logger
import numpy as np


def load_npz(path):
  """
  Load npz file into dict and logging their shapes to info.
  """
  path = Path(path)
  logger.info('Loading npz file {}...'.format(str(path)))
  data = np.load(path)
  result = {}
  for k in data:
    result[k] = np.array(data[k])
    logger.info('Field: {}, shape: {}.'.format(k, result[k].shape))
  return result
