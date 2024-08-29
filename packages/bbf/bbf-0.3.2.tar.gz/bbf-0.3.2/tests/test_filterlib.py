#!/usr/bin/env python3

# import numpy as np
# from lemaitre import bandpasses
from bbf.filterlib import FilterLib

import pytest


# def random_sensor_id(band, size):
#     if 'megacam6' in band:
#         return np.random.choice(np.arange(0, 36), size)
#     if 'hsc' in band:
#         return np.random.choice(np.arange(0, 103), size)
#     if 'ztf' in band:
#         return np.random.choice(np.arange(1, 65), size)
#     return None


# def test_check_args(nmeas=100_000):
#     """
#     """
#     fl = bandpasses.get_filterlib()
#     star = np.random.randint(131, size=nmeas)
#     band = np.random.choice(fl.bandpass_names, size=nmeas)
#     x = np.random.uniform(0., 3000., nmeas)
#     y = np.random.uniform(0., 3000., nmeas)
#     sensor_id = np.zeros(nmeas).astype(int)

#     for b in np.unique(band):
#         idx = band == b
#         sensor_id[idx] = random_sensor_id(b, idx.sum())

#     return fl, star, band, x, y, sensor_id


@pytest.mark.parametrize('compression', (None, 'lzma', 'bzip2'))
def test_save_load(tmp_path, compression):
    flib = FilterLib()

    filename = tmp_path / 'flib.pkl'
    flib.save(filename, compression=compression)

    filename = filename.with_suffix({
        None: '.pkl',
        'lzma': '.pkl.xz',
        'bzip2': '.pkl.bz2'}[compression])
    flib2 = FilterLib.load(filename)
