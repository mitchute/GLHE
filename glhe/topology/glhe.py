from glhe.topology.path import Path


class GLHE(object):

    def __init__(self, inputs):
        self._name = inputs["name"]
        self._paths = []
        for path in inputs["paths"]:
            self._paths.append(Path(path))

    def simulate(self):
        pass
