import os
import sys

sys.path.insert(0, os.path.abspath('../../..'))

from glhe.globals.constants import SEC_IN_YEAR  # noqa
from studies.aggregation.scripts.write_pbs import write_pbs  # noqa
from studies.aggregation.static.setup_static_cases import write_static_json_input  # noqa

run_times = [SEC_IN_YEAR, 5 * SEC_IN_YEAR]
loads = ['balanced', 'imbalanced']
wall_times = ['20:00', '1:30:00']

bin_widths = [[1, 48, 144, 432],
              [1, 48, 144, 288],
              [1, 48, 192, 384]]

min_num_bins = [[12, 4, 3, 3],
                [12, 4, 3, 2],
                [12, 4, 4, 3]]

# shortcuts
join = os.path.join
norm = os.path.normpath
cwd = os.getcwd()


def setup_all_cases():
    for _, load in enumerate(loads):
        for idx_time, time in enumerate(run_times):

            load_time_name = '{}_{}'.format(load, int(time / SEC_IN_YEAR))

            for idx_num, num_hourly in enumerate(min_num_bins):
                for idx_w, width in enumerate(bin_widths):

                    run_name = '{}_{}'.format(idx_num, idx_w)
                    run_path = join(cwd, 'runs', load_time_name, run_name)

                    if not os.path.exists(run_path):
                        os.makedirs(run_path)

                    load_path = '{}.csv'.format(norm(join(cwd, '../base', load)))
                    g_path = norm(join(cwd, '../base', 'g_functions.csv'))
                    output_path = join(run_path, 'out.csv')

                    other_inputs = {'bin widths in hours': width,
                                    'min number bins': num_hourly}

                    write_static_json_input(run_path, time, load_path, g_path, output_path, other_inputs)
                    write_pbs(run_path, wall_times[idx_time], 6)


def set_dynamic_parameters():
    pass


if __name__ == "__main__":
    setup_all_cases()
