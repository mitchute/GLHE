import os
import sys


def _append_path(num_up):
    path_str = ''
    for i in range(num_up):
        path_str += '../'
    sys.path.insert(0, os.path.abspath(path_str))


if __name__ == "__main__":
    _append_path(sys.argv[2])
    from standalone.run_g_function import RunGFunctions  # noqa

    RunGFunctions(sys.argv[1]).simulate()
