import fnmatch
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath('../../..'))

from glhe.globals.constants import SEC_IN_HOUR  # noqa
from glhe.globals.constants import SEC_IN_MIN  # noqa
from glhe.globals.functions import load_json  # noqa
from glhe.globals.constants import SEC_IN_YEAR  # noqa

# shortcuts
cwd = os.getcwd()
join = os.path.join
norm = os.path.normpath
split = os.path.split


def os_path_split_asunder(path, debug=False):
    # https://stackoverflow.com/questions/4579908/cross-platform-splitting-of-path-in-python

    parts = []
    while True:
        newpath, tail = split(path)
        if debug:
            print(repr(path), (newpath, tail))
        if newpath == path:
            assert not tail
            if path:
                parts.append(path)
            break
        parts.append(tail)
        path = newpath
    parts.reverse()
    return parts


def calc_rmse(file_1, file_2):
    df1 = pd.read_csv(file_1, usecols=[1], names=["Base"], header=0, dtype=np.float64)
    df2 = pd.read_csv(file_2, usecols=[1], names=["Case"], header=0, dtype=np.float64)
    df = pd.concat([df1, df2], axis=1)
    return ((df['Base'] - df['Case']) ** 2).mean() ** 0.5


def get_base_run_file_path(path):
    d = load_json(path)
    load_path_str = d['flow-profile']['external']['path']
    load = os_path_split_asunder(load_path_str)[-1].split(".")[0]
    time = int(d['simulation']['runtime'] / SEC_IN_YEAR)

    this_file_path = os.path.dirname(__file__)

    path_to_base_run_file = norm(join(this_file_path,
                                      '..',
                                      'none',
                                      'runs',
                                      '{}_{}'.format(load, time),
                                      'out.csv'))

    if not os.path.exists(path_to_base_run_file):
        raise FileNotFoundError

    return path_to_base_run_file, load, time


def get_run_time(path):
    time_str = ''
    hrs = 0
    mins = 0
    secs = 0
    count = 0

    for _, _, files in os.walk(path):
        for file in files:
            if fnmatch.fnmatch(file, '*.pbs.*'):
                with open(join(path, file), 'r') as f:
                    for line in f:
                        if 'Final runtime:' in line:
                            line = line.split('Final runtime:')[-1]
                            time_str = line.replace(' ', '')
                            tokens = time_str.split(':')
                            hrs += float(tokens[0])
                            mins += float(tokens[1])
                            secs += float(tokens[2])
                            count += 1
                            break

    return hrs / count * SEC_IN_HOUR + mins / count * SEC_IN_MIN + secs / count


def compute_run_stats(path):
    base_path, load, sim_time = get_base_run_file_path(join(path, 'in.json'))
    rmse = calc_rmse(base_path, join(path, 'out.csv'))
    run_time = get_run_time(path)
    return run_time, rmse, load, sim_time
