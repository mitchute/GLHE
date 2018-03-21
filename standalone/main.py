import json
import sys

from glhe.topology.glhe import GLHE

if __name__ == '__main__':

    with open(sys.argv[1]) as f:
        json_blob = f.read()

    d = json.loads(json_blob)
    g = GLHE(d)
    g.simulate(10, 1, 300)
