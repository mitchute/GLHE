import os

from jsonschema import SchemaError, ValidationError, validate
from glhe.globals.functions import lower_obj
from glhe.globals.functions import load_json, lower_obj
from glhe.properties.definition_manager import DefinitionsMGR
from glhe.properties.props_manager import PropsMGR


class InputProcessor(object):

    def __init__(self, json_input_path: str) -> None:
        """
        Initialize the input processor, process input file, and store the input information.

        :raises FileNotFoundError when input file not found.

        :param json_input_path: input file path
        :return none
        """

        # check if file exists
        if not os.path.exists(json_input_path):
            raise FileNotFoundError("Input file: '{}' does not exist.".format(json_input_path))

        # load the input file
        self.inputs = lower_obj(load_json(json_input_path))

        # validate the inputs
        self.validate_inputs(self.inputs)

        # load definitions for later use
        self.defs_mgr = DefinitionsMGR()
        self.defs_mgr.load_definitions(self.inputs)

        # load properties for later use
        self.props_mgr = PropsMGR()
        self.props_mgr.load_properties(self.inputs)

    @staticmethod
    def validate_inputs(input_dict: dict) -> None:
        """
        Validates the input objects against the schema.

        :param input_dict: input object
        :return: none
        """

        # shortcut
        fpath = os.path.join

        for key, value in input_dict.items():
            # load proper the schema
            schema_path = fpath(os.path.dirname(os.path.abspath(__file__)), 'schema')
            schema = load_json(fpath(schema_path, '{}.jsonschema'.format(key)))

            # validate
            try:
                validate(lower_obj(value), lower_obj(schema))
            except ValidationError:
                raise ValidationError("Input object '{}' is invalid.".format(key))
            except SchemaError:
                raise SchemaError("Schema for object '{}' is invalid.".format(key))
