import fnmatch
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath('../../..'))

from glhe.globals.constants import SEC_IN_HOUR  # noqa
from glhe.globals.constants import SEC_IN_MIN  # noqa
from glhe.globals.constants import SEC_IN_DAY  # noqa
from glhe.globals.functions import load_json  # noqa
from glhe.globals.constants import SEC_IN_YEAR  # noqa

# shortcuts
cwd = os.getcwd()
join = os.path.join
norm = os.path.normpath
split = os.path.split


def os_path_split_asunder(path, debug=False):
    # https://stackoverflow.com/questions/4579908/cross-platform-splitting-of-path-in-python

    if os.path.exists(path):
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
    else:
        print("File not found: {}".format(path))
        raise FileNotFoundError


def calc_rmse(file_1, file_2):
    df1 = pd.read_csv(file_1, usecols=["Average Fluid Temp [C]"], dtype=np.float64)
    df1.rename(index=str, columns={"Average Fluid Temp [C]": "Base"}, inplace=True)

    df2 = pd.read_csv(file_2, usecols=["Average Fluid Temp [C]"], dtype=np.float64)
    df2.rename(index=str, columns={"Average Fluid Temp [C]": "Test"}, inplace=True)

    df = pd.concat([df1, df2], axis=1)
    return ((df['Base'] - df['Test']) ** 2).mean() ** 0.5


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
                                      '{}_{}'.format(load, time)))

    if not os.path.exists(path_to_base_run_file):
        raise FileNotFoundError

    return path_to_base_run_file, load, time


def get_run_time(path):

    count = 0

    results = []

    for _, _, files in os.walk(path):
        for file in files:
            if fnmatch.fnmatch(file, '*.pbs.*'):
                with open(join(path, file), 'r') as f:
                    for line in f:
                        if 'Final runtime:' in line:
                            line = line.split('Final runtime:')[-1]
                            line = line.replace(' ', '')
                            if 'day' in line or 'days' in line:
                                tokens = line.split(',')
                                if 'days' in line:
                                    days = float(tokens[0].replace('days', ''))
                                elif 'day' in line:
                                    days = float(tokens[0].replace('day', ''))
                                else:
                                    days = 0

                                line = tokens[-1]

                            else:
                                days = 0

                            tokens = line.split(':')

                            hrs = float(tokens[0])
                            mins = float(tokens[1])
                            secs = float(tokens[2])

                            time = days * SEC_IN_DAY + hrs * SEC_IN_HOUR + mins * SEC_IN_MIN + secs

                            results.append(time)
                            count += 1

                            break

    try:
        return np.mean(results), np.std(results), len(results)
    except ZeroDivisionError:
        return 0, 0, 0


def compute_run_stats(path, base_path=None):

    if base_path is None:
        base_path, load, sim_time = get_base_run_file_path(join(path, 'in.json'))
    else:
        load = 'balanced'
        sim_time = 1

    rmse = calc_rmse(join(base_path, 'out.csv'), join(path, 'out.csv'))
    run_time, run_time_stdev, sample_count = get_run_time(path)
    base_run_time, _, _ = get_run_time(base_path)

    try:
        run_time_frac = run_time / base_run_time
    except ZeroDivisionError:
        run_time_frac = 0
        print('Base runtime error: {}'.format(base_path))

    return run_time, run_time_frac, run_time_stdev, rmse, load, sim_time, sample_count
