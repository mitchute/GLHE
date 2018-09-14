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
    pt_1 = tokens[-2]
    pt_2 = tokens[-1]
    return pt_1, pt_2


def process_all_run_stats(path_to_root):
    cols = ['run time', 'rmse', 'load', 'sim_time', 'min hourly', 'min other']

    df = pd.DataFrame(columns=cols)

    for dirpath, subdirs, files in os.walk(path_to_root):
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
                    df = pd.concat([df, df_case], ignore_index=True)

                    with open(join(path_to_root, 'static_stats.log'), 'a') as f:
                        f.write('{} completed\n'.format(this_dir))

                except FileNotFoundError:
                    pass

            elif run_exists and not log_exists:
                print("'{}' run not completed".format(this_dir))

    df.to_csv(join(path_to_root, "static_stats.csv"))


if __name__ == "__main__":
    process_all_run_stats(sys.argv[1])