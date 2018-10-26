import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath('../../..'))

from studies.aggregation.scripts.process_stats_scripts import compute_run_stats  # noqa
from studies.aggregation.scripts.process_stats_scripts import os_path_split_asunder  # noqa

# shortcuts
join = os.path.join


def get_configuration(path):
    tokens = os_path_split_asunder(path)
    tokens = tokens[-2].split('_')
    return float(tokens[0]), float(tokens[1]), float(tokens[2])


def process_all_run_stats(path_to_root):
    cols = ['run time',
            'run time fraction',
            'run time stdev',
            'rmse',
            'load',
            'sim time',
            'conductivity',
            'density',
            'cp',
            'sample count']

    fpath_csv = join(path_to_root, "soil_stats.csv")
    fpath_log = join(path_to_root, "soil_stats.log")

    if os.path.exists(fpath_log):
        os.remove(fpath_log)

    df = pd.DataFrame(columns=cols)

    for dirpath, subdirs, files in os.walk(path_to_root):
        for subdir in subdirs:

            if subdir == 'annual' or subdir == 'test':
                break

            test_dir = join(dirpath, subdir, 'test')
            annual_dir = join(dirpath, subdir, 'annual')

            test_run_exists = os.path.exists(join(test_dir, "run.pbs"))
            test_log_exists = os.path.exists(join(test_dir, "out.log"))

            annual_run_exists = os.path.exists(join(annual_dir, "run.pbs"))
            annual_log_exists = os.path.exists(join(annual_dir, "out.log"))

            if test_run_exists and test_log_exists and annual_run_exists and annual_log_exists:

                try:
                    run_time, run_time_frac, run_time_stdev, rmse, load, sim_time, sample_count = compute_run_stats(
                        test_dir, base_path=annual_dir)

                    k, rho, cp = get_configuration(test_dir)

                    d = {cols[0]: [run_time],
                         cols[1]: [run_time_frac],
                         cols[2]: [run_time_stdev],
                         cols[3]: [rmse],
                         cols[4]: [load],
                         cols[5]: [sim_time],
                         cols[6]: [k],
                         cols[7]: [rho],
                         cols[8]: [cp],
                         cols[9]: [sample_count]}

                    df_case = pd.DataFrame(data=d)
                    df = pd.concat([df, df_case], ignore_index=True)

                    with open(fpath_log, 'a') as f:
                        f.write('{} completed\n'.format(test_dir))

                except FileNotFoundError:
                    pass

            elif test_run_exists and not test_log_exists:
                print("'{}' run not completed".format(test_dir))
            elif annual_run_exists and not annual_log_exists:
                print("'{}' base run not completed".format(annual_dir))

    if os.path.exists(fpath_csv):
        os.remove(fpath_csv)
    df.to_csv(fpath_csv)


if __name__ == "__main__":
    process_all_run_stats(sys.argv[1])
