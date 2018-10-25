import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath('../../..'))

from glhe.globals.constants import SEC_IN_YEAR  # noqa
from glhe.globals.constants import SEC_IN_HOUR  # noqa
from studies.aggregation.scripts.write_pbs import write_pbs  # noqa
from glhe.globals.functions import load_json, write_json  # noqa

change = np.arange(0.8, 1.3, step=0.1)

k_vals = 2.7 * change
rho_vals = 2500 * change
cp_vals = 880 * change

# shortcuts
join = os.path.join
norm = os.path.normpath
cwd = os.getcwd()


def setup_all_cases():
    time = 1 * SEC_IN_YEAR
    load = 'balanced'
    wall_time = '1:00:00'
    exp_rate = 1.25
    start_width = 1
    end_width = 1

    for idx_k, k in enumerate(k_vals):
        for idx_rho, rho in enumerate(rho_vals):
            for idx_cp, cp in enumerate(cp_vals):

                depth, exp_rate, start_width, end_width = set_dynamic_parameters(time,
                                                                                 exp_rate,
                                                                                 start_width,
                                                                                 end_width)

                run_name = '{:0.1f}_{:0.0f}_{:0.0f}'.format(k, rho, cp)
                run_path = join(cwd, 'runs', run_name, 'test')
                run_path_annual = join(cwd, 'runs', run_name, 'annual')

                if not os.path.exists(run_path):
                    os.makedirs(run_path)

                if not os.path.exists(run_path_annual):
                    os.makedirs(run_path_annual)

                load_path = '{}.csv'.format(norm(join(cwd, '../base', load)))
                g_path = norm(join(cwd, '../base', 'g_functions.csv'))
                output_path = join(run_path, 'out.csv')
                output_path_annual = join(run_path_annual, 'out_annual.csv')

                other_inputs = {'depth': depth,
                                'expansion rate': exp_rate,
                                'start width': start_width,
                                'end width': end_width,
                                'k': k,
                                'rho': rho,
                                'cp': cp}

                write_soil_json_input(run_path, time, load_path, g_path, output_path, other_inputs)
                write_annual_json_input(run_path_annual, time, load_path, g_path, output_path_annual, other_inputs)
                write_pbs(run_path, wall_time, 6, False)
                write_pbs(run_path_annual, wall_time, 6, False)


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


def write_annual_json_input(run_dir, time, path_to_load, path_to_g, path_to_output, other):
    f = load_json(norm(join(cwd, '../base', 'base_case.json')))
    f['flow-profile']['external']['path'] = path_to_load
    f['load-profile']['external']['path'] = path_to_load
    f['g-functions']['file'] = path_to_g
    f['simulation']['runtime'] = time
    f['simulation']['output-path'] = path_to_output

    f['load-aggregation']['type'] = 'none'

    f['soil']['conductivity'] = other['k']
    f['soil']['density'] = other['rho']
    f['soil']['specific heat'] = other['cp']

    write_json(join(run_dir, 'in.json'), f)


def write_soil_json_input(run_dir, time, path_to_load, path_to_g, path_to_output, other):
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

    f['soil']['conductivity'] = other['k']
    f['soil']['density'] = other['rho']
    f['soil']['specific heat'] = other['cp']

    write_json(join(run_dir, 'in.json'), f)


if __name__ == "__main__":
    setup_all_cases()
