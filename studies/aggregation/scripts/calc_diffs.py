import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath('../../../../../../..'))

from glhe.globals.functions import load_json

# shortcuts
cwd = os.getcwd()
join = os.path.join


def os_path_split_asunder(path, debug=False):
    # https://stackoverflow.com/questions/4579908/cross-platform-splitting-of-path-in-python

    parts = []
    while True:
        newpath, tail = os.path.split(path)
        if debug: print(repr(path), (newpath, tail))
        if newpath == path:
            assert not tail
            if path: parts.append(path)
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


def get_base_file_path(path):
    d = load_json(path)
    load_path_str = d['flow-profile']['external']['path']
    load = os_path_split_asunder(load_path_str)[0]

    pass


def compute_stats(path):
    base_path = get_base_file_path(join(cwd, 'in.json'))


if __name__ == "__main__":
    if not os.path.exists(sys.argv[1]):
        print("'{}' file does not exist".format(sys.argv[1]))
    else:
        try:
            compute_stats(sys.argv[1])
        except:
            print("'{}' failed".format(sys.argv[1]))
