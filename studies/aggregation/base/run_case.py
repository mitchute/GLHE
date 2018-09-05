import os
import sys

sys.path.insert(0, os.path.abspath('../../../../..'))

from standalone.run_g_function import RunGFunctions  # noqa

if __name__ == "__main__":
    RunGFunctions(sys.argv[1]).simulate()
