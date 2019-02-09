import os
import sys

from jsonschema import validate

from glhe.globals.functions import load_json
from glhe.properties.definition_manager import DefinitionsMGR
from glhe.properties.props_manager import PropsMGR


class InputProcessor(object):

    def __init__(self):
        self.definition_mgr = None
        self.props_mgr = None

    def process_input(self, json_input_path: str) -> dict:
        """
        Process input file

        :param json_input_path: input file path
        :return: expanded input file
        """

        # check if file exists
        if not os.path.exists(json_input_path):
            raise FileNotFoundError("Input file: '{}' does not exist".format(sys.argv[1]))

        # load the input file
        d = load_json(json_input_path)

        # validate the inputs
        self._validate_inputs(d)

        # load definitions for later use
        self.definition_mgr = DefinitionsMGR()
        self.definition_mgr.load_definitions(d)

        # load properties for later use
        self.props_mgr = PropsMGR()
        self.props_mgr.load_properties(d)

        return d

    @staticmethod
    def _validate_inputs(input_dict: dict) -> None:
        """
        Validates the input objects against the schema

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
                validate(value, schema)
            except ValueError:
                raise ValueError("Input object '{}' cannot validate against the schema".format(key))
