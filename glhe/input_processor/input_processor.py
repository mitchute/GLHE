from json import loads
import os
from pathlib import Path

from jsonschema import SchemaError, ValidationError, validate

from glhe.ground_temps.ground_temp_factory import make_ground_temp_model
from glhe.properties.fluid_factory import get_fluid
from glhe.properties.base_properties import PropertiesBase
from glhe.functions import load_json, lower_obj


class InputProcessor:

    def __init__(self, json_input_path: Path):
        """
        Initialize the input processor, process input file, and store the input information.

        :raises: FileNotFoundError when input file not found.

        :param json_input_path: input file path
        """

        # check if file exists
        if not json_input_path.exists():
            raise FileNotFoundError(f"Input file: '{json_input_path}' does not exist.")

        # load the input file
        self.input_dict: dict = lower_obj(loads(json_input_path.read_text()))

        # validate the inputs
        self.validate_inputs(self.input_dict)

        # load properties for later use
        try:
            self.fluid = get_fluid(self.input_dict['fluid'])
        except KeyError:
            pass

        try:
            self.soil = PropertiesBase(self.input_dict['soil'])
            try:
                self.soil.get_temp = make_ground_temp_model(self.input_dict['ground-temperature-model']).get_temp
            except KeyError:
                pass

        except KeyError:
            pass

    @staticmethod
    def validate_inputs(input_dict: dict) -> None:
        """
        Validates the input objects against the schema.

        :param input_dict: input object

        :raises: ValidationError if the input object is not correct
        :raises: SchemaError is the schema is not correct
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
                raise ValidationError("Input object '{}' is not valid.".format(key))
            except SchemaError:  # pragma: no cover
                raise SchemaError("Schema for object '{}' is not valid.".format(key))  # pragma: no cover

    def get_definition_object(self, obj_type_to_find: str, obj_name: str) -> dict:
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

        raise KeyError("Object type: '{}', Name: '{}' not found.".format(obj_type_to_find, obj_name))

    def init_temp(self):
        """
        Initial temperature for all temperature variables. Valid at t=0.

        :return: Initial temperature
        """
        try:
            return self.input_dict['simulation']['initial-temperature']
        except KeyError:
            return 20
