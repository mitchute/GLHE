import os
import sys

sys.path.insert(0, os.path.abspath('../../..'))

from glhe.globals.constants import SEC_IN_YEAR  # noqa
from glhe.globals.functions import load_json, write_json  # noqa

run_times = [SEC_IN_YEAR, 5 * SEC_IN_YEAR]
loads = ['balanced', 'imbalanced']
wall_times = ['3:00:00', '30:00:00']

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


def write_pbs(run_dir, time):
    pbs = ''

    with open(norm(join(cwd, '../base', 'run.pbs')), 'r') as f:
        for line in f:
            if 'SIM_RUNTIME' in line:
                pbs += line.replace('SIM_RUNTIME', time)
            elif 'PATH_TO_LOCAL_JSON_FILE' in line:
                pbs += line.replace('PATH_TO_LOCAL_JSON_FILE', join(run_dir, 'in.json'))
            else:
                pbs += line

    with open(join(run_dir, 'run.pbs'), 'w') as f:
        f.write(pbs)


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
            write_no_agg_json_input(run_path, time, load_path, g_path, output_path)
            write_pbs(run_path, wall_times[idx])


if __name__ == "__main__":
    setup_case()
