import os

from glhe.globals.constants import SEC_IN_YEAR
from glhe.globals.functions import load_json, write_json
from standalone.run_g_function import RunGFunctions

run_times = [SEC_IN_YEAR, 20 * SEC_IN_YEAR]
loads = ['balanced', 'imbalanced']


def write_case_input(time, load):
    f = load_json('base_case.json')
    f['flow-profile']['external']['path'] = '{}.csv'.format(os.path.join(os.getcwd(), load))
    f['load-profile']['external']['path'] = '{}.csv'.format(os.path.join(os.getcwd(), load))
    f['g-functions']['file'] = '{}.csv'.format(os.path.join(os.getcwd(), 'g_functions'))
    f['simulation']['runtime'] = time

    file_name = '{}_{}.csv'.format(load, str(int(time / SEC_IN_YEAR)))

    f['simulation']['output-path'] = os.path.join(os.getcwd(), file_name)
    write_json(os.path.join(os.getcwd(), 'in.json'), f)


if __name__ == "__main__":

    for time in run_times:
        for load in loads:
            write_case_input(time, load)
            RunGFunctions(os.path.join(os.getcwd(), "in.json")).simulate()
