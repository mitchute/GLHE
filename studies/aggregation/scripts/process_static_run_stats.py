import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath('../../..'))

from glhe.globals.functions import load_json  # noqa
from glhe.globals.constants import SEC_IN_YEAR  # noqa
from glhe.globals.constants import SEC_IN_HOUR  # noqa
from glhe.globals.constants import SEC_IN_MIN  # noqa

# shortcuts
cwd = os.getcwd()
join = os.path.join
norm = os.path.normpath


def os_path_split_asunder(path, debug=False):
    # https://stackoverflow.com/questions/4579908/cross-platform-splitting-of-path-in-python

    parts = []
    while True:
        newpath, tail = os.path.split(path)
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
    with open(path, 'r') as f:
        for line in f:
            time_str = line.replace(' ', '')
            break

    tokens = time_str.split(':')
    hrs = float(tokens[1])
    mins = float(tokens[2])
    secs = float(tokens[3])

    return hrs * SEC_IN_HOUR + mins * SEC_IN_MIN + secs


def compute_run_stats(path):
    base_path, load, sim_time = get_base_run_file_path(join(path, 'in.json'))
    rmse = calc_rmse(base_path, join(path, 'out.csv'))
    run_time = get_run_time(join(path, 'out.log'))
    return run_time, rmse, load, sim_time


def get_configuration(path):
    tokens = os_path_split_asunder(path)
    pt_1 = tokens[-2]
    pt_2 = tokens[-1]
    return pt_1, pt_2


def process_all_run_stats(path):
    cols = ['run time', 'rmse', 'load', 'sim_time', 'min hourly', 'min other']

    df = pd.DataFrame(columns=cols)

    for dirpath, subdirs, files in os.walk(path):
        for subdir in subdirs:

            this_dir = join(dirpath, subdir)
            run_exists = os.path.exists(join(this_dir, "run.pbs"))
            log_exists = os.path.exists(join(this_dir, "out.log"))

            if run_exists and log_exists:

                try:
                    run_time, rmse, load, sim_time = compute_run_stats(this_dir)
                    config_1, config_2 = get_configuration(this_dir)

                    d = {cols[0]: [run_time],
                         cols[1]: [rmse],
                         cols[2]: [load],
                         cols[3]: [sim_time],
                         cols[4]: [config_1],
                         cols[5]: [config_2]}

                    df_case = pd.DataFrame(data=d)
                    df = pd.concat([df, df_case])

                    with open('static_stats.log', 'a') as f:
                        f.write('{} completed\n'.format(this_dir))

                except FileNotFoundError:
                    pass

            elif run_exists and not log_exists:
                print("'{}' run not completed".format(this_dir))

    df.to_csv("static_stats.csv")


if __name__ == "__main__":
    process_all_run_stats(sys.argv[1])
