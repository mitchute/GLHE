import os
import sys

from glhe.globals.functions import load_json

from jsonschema import validate


fpath = os.path.join


class InputProcessor(object):

    def __init__(self):
        self.definitions = {}

    def process_input(self, input_file_path):
        """
        Process input file

        :param input_file_path: input file path
        :return: expanded input file
        """

        # load the input file
        d = load_json(input_file_path)

        # load the schema
        schema = load_json(fpath(os.getcwd(), 'schema.json'))

        # validate
        validate(d, schema)

        # get the definitions so we can use them to expand
        del_keys = []
        for key, value in d.items():
            if "definitions" in key:
                tokens = key.split('-')
                def_key = tokens[0]
                self.definitions[def_key] = value
                del_keys.append(key)

        # don't need the defs here anymore, so get rid of them
        for item in del_keys:
            del d[item]

        # expand objects
        return self.expand_dict(d)

    def expand_dict(self, inputs):
        """
        Expands dictionary objects by iterating over all key-value pairs.

        Only keys containing the "-type" string should be expanded.

        :param inputs: compressed dictionary object
        :return: expanded dictionary object
        """

        d_ret = {}
        for key, value in inputs.items():
            if type(value) is dict:
                d_ret[key] = self.expand_dict(value)
            elif type(value) is list:
                d_ret[key] = self.expand_list(value)
            else:
                if "-type" in key:
                    tokens = key.split('-')
                    def_type = tokens[0]
                    def_name = value
                    new_key = '{}-data'.format(def_type)
                    new_val = self.get_input_definition_data(def_type, def_name)
                    d_ret[new_key] = self.expand_dict(new_val)
                else:
                    d_ret[key] = value

        return d_ret

    def expand_list(self, inputs):
        """
        Expands list objects by iterating over all items in the list.

        Expandable items are only found in dictionaries, no "expansion" is done here.

        :param inputs: list object with compressed inputs
        :return: list object with expanded inputs
        """

        l_ret = []
        for item in inputs:
            if type(item) is dict:
                l_ret.append(self.expand_dict(item))
            elif type(item) is list:
                l_ret.append(self.expand_list(item))
            else:
                l_ret.append(item)

        return l_ret

    def get_input_definition_data(self, definition_type, definition_name):
        """
        Searches the definitions lists for a matching name. If found, return
        so the object can be expanded.

        :param definition_type: type of definition
        :param definition_name: name of definition
        :return: found object
        """

        for d_type, d_val in self.definitions.items():
            if d_type == definition_type:
                for obj in d_val:
                    if obj['type-name'] == definition_name:
                        return obj

        raise ValueError("'{}' definition not found".format(definition_name))

if __name__ == "__main__":
    obj = InputProcessor().process_input(sys.argv[1])
    pass
