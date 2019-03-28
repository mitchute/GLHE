import os

from jsonschema import SchemaError, ValidationError, validate

from glhe.globals.functions import load_json, lower_obj
from glhe.properties.props_manager import PropsMGR


class InputProcessor(object):

    def __init__(self, json_input_path: str) -> None:
        """
        Initialize the input processor, process input file, and store the input information.

        :raises FileNotFoundError when input file not found.

        :param json_input_path: input file path
        """

        # check if file exists
        if not os.path.exists(json_input_path):
            raise FileNotFoundError("Input file: '{}' does not exist.".format(json_input_path))

        # load the input file
        self.input_dict = lower_obj(load_json(json_input_path))

        # validate the inputs
        self.validate_inputs(self.input_dict)

        # load properties for later use
        self.props_mgr = PropsMGR()
        self.props_mgr.load_properties(self.input_dict)

    @staticmethod
    def validate_inputs(input_dict: dict) -> None:
        """
        Validates the input objects against the schema.

        :param input_dict: input object

        :raises ValidationError if the input object is not correct
        :raises SchemaError is the schema is not correct
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

    def get_input_object(self, obj_type_to_find: str, obj_name: str) -> dict:
        """
        Loads the definitions for the boreholes, grout, and pipe.

        :param obj_type_to_find:
        :param obj_name:
        """

        for obj_type in self.input_dict:
            if obj_type_to_find == obj_type:
                for obj in self.input_dict[obj_type_to_find]:
                    if obj['name'] == obj_name:
                        return obj

        raise NotImplementedError("Object type: '{}', Name: '{}' not found.".format(obj_type_to_find, obj_name))

    def init_temp(self):
        """
        Initial temperature for all temperature variables. Valid at t=0.

        :return: Initial temperature
        """
        try:
            return self.input_dict['simulation']['initial-temperature']
        except KeyError:
            return 20
