import h5py
import numpy as np
import pandas as pd


def _load_h5_data(path_file, path_dataset):
  with h5py.File(path_file, 'r') as fin:
    data = np.array(fin[path_dataset])
    if data.ndim == 3:
      data = np.expand_dims(data, 3)
    return data


def _to_ndarray(input_):
  if input_ is None:
    return input_
  if isinstance(input_, np.ndarray):
    return input_
  if isinstance(input_, dict):
    if input_['type'] == 'h5':
      return _load_h5_data(input_['path_file'], input_['path_dataset'])
  raise ValueError("Can't convert {} to ndrray.".format(input_))


def metric(name_or_method):
  from .image import psnr, ssim, msssim, rmse
  if isinstance(name_or_method, str):
    return {
        'mean': np.mean,
        'max': np.max,
        'min': np.min,
        'std': np.std,
        'ssim': ssim,
        'psnr': psnr,
        'msssim': msssim,
        'rmse': rmse,
    }[name_or_method]
  return name_or_method


def analysis(target,
             label=None,
             single_analysis_metrics=None,
             compare_analysis_metrics=None,
             output_csv=None,
             *,
             denorm=None):
  from .image import single_analysis, compare_analysis
  target = _to_ndarray(target)
  if denorm is not None:
    target = target * denorm['std'] + denorm['mean']
  label = _to_ndarray(label)
  if single_analysis_metrics is not None:
    single_analysis_metrics = [metric(s) for s in single_analysis_metrics]
  if compare_analysis_metrics is not None:
    compare_analysis_metrics = [metric(m) for m in compare_analysis_metrics]
  results = []
  if single_analysis_metrics is not None:
    results.append(single_analysis(target, single_analysis_metrics))
  if compare_analysis_metrics is not None:
    results.append(compare_analysis(label, target, compare_analysis_metrics))
  result = pd.concat(results, axis=1)
  if output_csv is not None:
    result.to_csv(output_csv)
  return result


def analysis_with_config(config_file):
  import json
  with open(config_file, 'r') as fin:
    c = json.load(fin)
  target = c.get('target')
  label = c.get('label')
  single_analysis_metrics = c.get('single')
  compare_analysis_metrics = c.get('compare')
  if single_analysis_metrics is not None:
    single_analysis_metrics = [metric(m) for m in single_analysis_metrics]
  if compare_analysis_metrics is not None:
    compare_analysis_metrics = [metric(m) for m in compare_analysis_metrics]
  return analysis(target, label, single_analysis_metrics,
                  compare_analysis_metrics, output_csv)
