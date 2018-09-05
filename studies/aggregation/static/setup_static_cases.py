import os
import sys

sys.path.insert(0, os.path.abspath('../../..'))

from glhe.globals.constants import SEC_IN_YEAR  # noqa
from glhe.globals.functions import load_json, write_json  # noqa
from studies.aggregation.base.write_pbs import write_pbs  # noqa

run_times = [SEC_IN_YEAR, 5 * SEC_IN_YEAR]
loads = ['balanced', 'imbalanced']
wall_times = ['1:00:00', '3:00:00']

bin_widths = [[1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384],
              [1, 3, 9, 27, 81, 243, 729, 2187, 6561, 19683],
              [1, 4, 16, 64, 256, 1024, 4096, 16384],
              [1, 5, 25, 125, 625, 3125, 15625],
              [1, 7, 49, 343, 2401, 16807],
              [1, 8, 64, 512, 4096],
              [1, 9, 81, 729, 6561],
              [1, 10, 100, 1000, 10000],
              [1, 11, 121, 1331, 14641],
              [1, 12, 144, 1728, 20736],
              [1, 13, 169, 2197],
              [1, 14, 196, 2744],
              [1, 15, 225, 3375],
              [1, 16, 256, 4096],
              [1, 17, 289, 4913],
              [1, 18, 324, 5832],
              [1, 19, 361, 6859],
              [1, 20, 400, 8000],
              [1, 21, 441, 9261],
              [1, 22, 484, 10648],
              [1, 23, 529, 12167],
              [1, 24, 576, 13824]]

min_num_bins_hourly = [1, 2, 4, 8, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
min_num_bins_others = 4

# shortcuts
join = os.path.join
norm = os.path.normpath
cwd = os.getcwd()


def write_static_json_input(run_dir, time, path_to_load, path_to_g, path_to_output):
    f = load_json(norm(join(cwd, '../base', 'base_case.json')))
    f['flow-profile']['external']['path'] = path_to_load
    f['load-profile']['external']['path'] = path_to_load
    f['g-functions']['file'] = path_to_g
    f['simulation']['runtime'] = time
    f['simulation']['output-path'] = path_to_output
    write_json(join(run_dir, 'in.json'), f)


def setup_case():
    for idx, time in enumerate(run_times):
        for load in loads:
            run_name = '{}_{}'.format(load, int(time / SEC_IN_YEAR))
            run_path = join(cwd, 'runs', run_name)
            if not os.path.exists(run_path):
                os.makedirs(run_path)
            load_path = '{}.csv'.format(norm(join(cwd, '../base', load)))
            g_path = norm(join(cwd, '../base', 'g_functions.csv'))
            output_path = join(run_path, 'out.csv')
            write_static_json_input(run_path, time, load_path, g_path, output_path)
            write_pbs(run_path, wall_times[idx])


def setup_all_cases():
    for width in bin_widths:
        for hour in min_num_bins_hourly:
            pass


if __name__ == "__main__":
    setup_all_cases()