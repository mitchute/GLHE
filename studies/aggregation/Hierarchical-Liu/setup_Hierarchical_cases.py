import os
import sys

sys.path.insert(0, os.path.abspath('../../..'))

from glhe.utilities.constants import SEC_IN_YEAR  # noqa
from studies.aggregation.scripts.write_pbs import write_pbs  # noqa
from studies.aggregation.static.setup_static_cases import write_static_json_input  # noqa

run_times = [1 * SEC_IN_YEAR,
             5 * SEC_IN_YEAR,
             10 * SEC_IN_YEAR]

loads = ['balanced', 'imbalanced']

wall_times = ['20:00',
              '2:00:00',
              '6:00:00']

bin_widths = [[1, 24, 120, 8760]]

min_num_bins = [[12, 3, 40, 3]]

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
                    write_pbs(run_path, wall_times[idx_time], 6, False)


if __name__ == "__main__":
    setup_all_cases()
