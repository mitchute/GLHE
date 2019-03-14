class DefinitionsMGR(object):

    def __init__(self) -> None:
        self.borehole_defs = []
        self.grout_defs = []
        self.pipe_defs = []

    def load_definitions(self, inputs: dict) -> None:
        for _, key in enumerate(inputs):
            if key == 'borehole-definitions':
                self._add_borehole_defs(inputs[key])
            elif key == 'grout-definitions':
                self._add_grout_defs(inputs[key])
            elif key == 'pipe-definitions':
                self._add_pipe_defs(inputs[key])

    def get_definition(self, def_type: str, name: str) -> dict:
        if def_type == 'borehole':
            return self._get_borehole_def(name)
        elif def_type == 'grout':
            return self._get_grout_def(name)
        elif def_type == 'pipe':
            return self._get_pipe_def(name)

    def _raise_def_not_found_error(self, name: str) -> None:
        raise KeyError("Definition '{}' not found.".format(name))

    def _get_borehole_def(self, name: str) -> dict:
        for definition in self.borehole_defs:
            if definition['name'] == name:
                return definition
        self._raise_def_not_found_error(name)

    def _get_grout_def(self, name: str) -> dict:
        for definition in self.grout_defs:
            if definition['name'] == name:
                return definition
        self._raise_def_not_found_error(name)

    def _get_pipe_def(self, name: str) -> dict:
        for definition in self.pipe_defs:
            if definition['name'] == name:
                return definition
        self._raise_def_not_found_error(name)

    def _add_borehole_defs(self, definitions):
        for _, definition in enumerate(definitions):
            new_def_name = definition['name']
            for existing_def in self.borehole_defs:
                if new_def_name == existing_def['name']:
                    raise ValueError("Borehole definition name '{}' already exists".format(new_def_name))
            self.borehole_defs.append(definition)

    def _add_grout_defs(self, definitions):
        for _, definition in enumerate(definitions):
            new_def_name = definition['name']
            for existing_def in self.grout_defs:
                if new_def_name == existing_def['name']:
                    raise ValueError("Grout definition name '{}' already exists".format(new_def_name))
            self.grout_defs.append(definition)

    def _add_pipe_defs(self, definitions):
        for _, definition in enumerate(definitions):
            new_def_name = definition['name']
            for existing_def in self.pipe_defs:
                if new_def_name == existing_def['name']:
                    raise ValueError("Pipe definition name '{}' already exists".format(new_def_name))
            self.pipe_defs.append(definition)
