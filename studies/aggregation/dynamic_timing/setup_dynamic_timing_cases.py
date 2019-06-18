import os
import sys

sys.path.insert(0, os.path.abspath('../../..'))

from glhe.utilities.constants import SEC_IN_YEAR  # noqa
from glhe.utilities.constants import SEC_IN_HOUR  # noqa
from studies.aggregation.scripts.write_pbs import write_pbs  # noqa
from glhe.utilities.functions import load_json, write_json  # noqa

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

wall_times = ['5:00',
              '10:00',
              '15:00',
              '20:00',
              '25:00',
              '30:00',
              '35:00',
              '40:00',
              '45:00',
              '50:00',
              '55:00',
              '60:00']

exp_rates = [1.25, 1.5, 1.61803398875, 1.75]
widths = [1, 5, 10]

# shortcuts
join = os.path.join
norm = os.path.normpath
cwd = os.getcwd()


def setup_all_cases():
    for _, load in enumerate(loads):
        for idx_time, time in enumerate(run_times):

            load_time_name = '{}_{}'.format(load, int(time / SEC_IN_YEAR))

            for idx_ex, exp_rate in enumerate(exp_rates):
                for idx_sw, width in enumerate(widths):
                    depth, exp_rate, start_width, end_width = set_dynamic_parameters(time, exp_rate, width,
                                                                                     width)

                    run_name = '{}_{}_{}'.format(depth, start_width, end_width)
                    run_path = join(cwd, 'runs', load_time_name, '{:0.2f}'.format(exp_rate), run_name)

                    if not os.path.exists(run_path):
                        os.makedirs(run_path)

                    load_path = '{}.csv'.format(norm(join(cwd, '../base', load)))
                    g_path = norm(join(cwd, '../base', 'g_functions.csv'))
                    output_path = join(run_path, 'out.csv')

                    other_inputs = {'depth': depth,
                                    'expansion rate': exp_rate,
                                    'start width': start_width,
                                    'end width': end_width}

                    write_dynamic_json_input(run_path, time, load_path, g_path, output_path, other_inputs)
                    write_pbs(run_path, wall_times[idx_time], 7, False)


def set_dynamic_parameters(run_time, exp_rate, start_width, end_width):
    _depth = 0
    _start_width = start_width
    _end_width = end_width

    while True:
        _depth += 1

        if start_width == "depth" and end_width == "depth":
            _start_width = _depth
            _end_width = _depth
        elif start_width == "depth" and end_width != "depth":
            _start_width = _depth
        elif start_width != "depth" and end_width == "depth":
            _end_width = _depth

        bins = make_bin_times(depth=_depth, exp_rate=exp_rate, start_width=_start_width, end_width=_end_width)

        available_time = sum(bins)

        if available_time > run_time:
            return _depth, exp_rate, _start_width, _end_width


def make_bin_times(depth, exp_rate, start_width, end_width):
    _loads = []
    for i in range(depth):
        width = int((1 - i / depth) * (start_width - end_width) + end_width)
        for _ in range(width):
            _loads.append(int(exp_rate ** i * SEC_IN_HOUR))
    return _loads


def write_dynamic_json_input(run_dir, time, path_to_load, path_to_g, path_to_output, other):
    f = load_json(norm(join(cwd, '../base', 'base_case.json')))
    f['flow-profile']['external']['path'] = path_to_load
    f['load-profile']['external']['path'] = path_to_load
    f['g-functions']['file'] = path_to_g
    f['simulation']['runtime'] = time
    f['simulation']['output-path'] = path_to_output

    f['load-aggregation']['type'] = 'dynamic'
    f['load-aggregation']['dynamic']['depth'] = other['depth']
    f['load-aggregation']['dynamic']['expansion rate'] = other['expansion rate']
    f['load-aggregation']['dynamic']['start width'] = other['start width']
    f['load-aggregation']['dynamic']['end width'] = other['end width']

    write_json(join(run_dir, 'in.json'), f)


if __name__ == "__main__":
    setup_all_cases()
