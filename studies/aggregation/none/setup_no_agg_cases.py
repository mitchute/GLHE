import os
import sys

sys.path.insert(0, os.path.abspath('../../..'))

from glhe.globals.constants import SEC_IN_YEAR  # noqa
from glhe.globals.functions import load_json, write_json  # noqa
from studies.aggregation.scripts.write_pbs import write_pbs  # noqa

run_times = [1 * SEC_IN_YEAR,
             2 * SEC_IN_YEAR,
             3 * SEC_IN_YEAR,
             4 * SEC_IN_YEAR,
             5 * SEC_IN_YEAR,
             6 * SEC_IN_YEAR,
             7 * SEC_IN_YEAR,
             8 * SEC_IN_YEAR,
             9 * SEC_IN_YEAR,
             10 * SEC_IN_YEAR,
             11 * SEC_IN_YEAR,
             12 * SEC_IN_YEAR]

loads = ['balanced', 'imbalanced']

wall_times = ['120:00:00',
              '120:00:00',
              '120:00:00',
              '120:00:00',
              '120:00:00',
              '504:00:00',
              '504:00:00',
              '504:00:00',
              '504:00:00',
              '504:00:00',
              '504:00:00',
              '504:00:00']

killable = [False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True]

# shortcuts
join = os.path.join
norm = os.path.normpath
cwd = os.getcwd()


def write_no_agg_json_input(run_dir, time, path_to_load, path_to_g, path_to_output):
    f = load_json(norm(join(cwd, '../base', 'base_case.json')))
    f['flow-profile']['external']['path'] = path_to_load
    f['load-profile']['external']['path'] = path_to_load
    f['g-functions']['file'] = path_to_g
    f['simulation']['runtime'] = time
    f['simulation']['output-path'] = path_to_output
    write_json(join(run_dir, 'in.json'), f)


def setup_all_cases():
    for idx, time in enumerate(run_times):
        for load in loads:
            run_name = '{}_{}'.format(load, int(time / SEC_IN_YEAR))
            run_path = join(cwd, 'runs', run_name)
            if not os.path.exists(run_path):
                os.makedirs(run_path)
            load_path = '{}.csv'.format(norm(join(cwd, '../base', load)))
            g_path = norm(join(cwd, '../base', 'g_functions.csv'))
            output_path = join(run_path, 'out.csv')
            write_no_agg_json_input(run_path, time, load_path, g_path, output_path)
            write_pbs(run_path, wall_times[idx], 5, killable[idx])


if __name__ == "__main__":
    setup_all_cases()
