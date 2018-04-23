import json
import sys

from glhe.topology.glhe import GLHE
from loads.bins.dynamic import DynamicBin

if __name__ == '__main__':

    # with open(sys.argv[1]) as f:
    #     json_blob = f.read()
    #
    # d = json.loads(json_blob)
    # g = GLHE(d)
    # g.simulate(10, 1, 300)

    # def temp_print(stuff):
    #     out = ''
    #     for j in range(15):
    #         out += '{} '.format(stuff.loads[j].energy)
    #
    #     return out

    d = DynamicBin(depth=10, start_width=10, end_width=1)
    d.add_load(1)

    # print(temp_print(d))
    #
    # for i in range(10):
    #     d.add_load(0)
    #     print(temp_print(d))

