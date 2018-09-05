import os
import sys

sys.path.insert(0, os.path.abspath('../../..'))

from standalone.run_g_function import RunGFunctions

if __name__ == "__main__":
    try:
        RunGFunctions(sys.argv[1])
        print("initialized")
    except:
        print("fail")
