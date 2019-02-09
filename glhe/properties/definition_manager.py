class DefinitionsMGR(object):
    borehole_defs = []
    grout_defs = []
    pipe_defs = []

    def __init__(self) -> None:
        pass

    @classmethod
    def load_definitions(cls, inputs: dict) -> None:
        for _, key in enumerate(inputs):
            if key == 'borehole-definitions':
                cls._add_borehole_defs(inputs[key])
            elif key == 'grout-definitions':
                cls._add_grout_defs(inputs[key])
            elif key == 'pipe-definitions':
                cls._add_pipe_defs(inputs[key])

    @classmethod
    def _add_borehole_defs(cls, definitions):
        for _, definition in enumerate(definitions):
            new_def_name = definition['name']
            for existing_def in cls.borehole_defs:
                if new_def_name == existing_def['name']:
                    raise ValueError("Borehole definition name '{}' already exists".format(new_def_name))
            cls.borehole_defs.append(definition)

    @classmethod
    def _add_grout_defs(cls, definitions):
        for _, definition in enumerate(definitions):
            new_def_name = definition['name']
            for existing_def in cls.grout_defs:
                if new_def_name == existing_def['name']:
                    raise ValueError("Grout definition name '{}' already exists".format(new_def_name))
            cls.grout_defs.append(definition)

    @classmethod
    def _add_pipe_defs(cls, definitions):
        for _, definition in enumerate(definitions):
            new_def_name = definition['name']
            for existing_def in cls.pipe_defs:
                if new_def_name == existing_def['name']:
                    raise ValueError("Pipe definition name '{}' already exists".format(new_def_name))
            cls.pipe_defs.append(definition)
