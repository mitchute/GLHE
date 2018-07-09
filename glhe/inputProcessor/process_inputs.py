import json


class InputProcessor(object):

    def __init__(self):
        self.definitions = {}

    def process_input(self, input_file_path):
        """
        Process input file

        :param input_file: input file path
        :return:
        """

        # read the file, parse the json
        with open(input_file_path) as f:
            json_blob = f.read()
        d = json.loads(json_blob)

        # get the definitions so we can use them to expand
        for key, value in d.items():
            if "definitions" in key:
                tokens = key.split('-')
                self.definitions[tokens[0]] = value

        # begin traversing the input to expand objects as needed
        out = {}
        for key, value in d.items():
            if "definitions" not in key:
                out[key] = self.expand_object(key, value)

        return out

    def expand_object(self, _key=None, _value=None):
        d_ret = {}
        if type(_value) is dict:
            for key, value in _value.items():
                d_ret[_key] = self.expand_object(key, value)
            return d_ret
        elif type(_value) is list:
            l_ret = []
            for entry in _value:
                l_ret.append(self.expand_object(_value=entry))
            return l_ret
        else:
            self.get_value(_key, _value)

        return d_ret

    def get_value(self, key, value):
        if "-type" in key:
            tokens = key.split('-')
            def_type = tokens[0]
            def_name = value
            new_key = '{}-data'.format(def_type)
            new_val = self.get_input_definition_data(def_type, def_name)
            return self.expand_object(new_key, new_val)
        else:
            return value

    def get_input_definition_data(self, definition_type, definition_name):

        for d_type, d_val in self.definitions.items():
            if d_type == definition_type:
                for obj in d_val:
                    if obj['type-name'] == definition_name:
                        return obj

        raise ValueError("'{}' definition not found".format(definition_name))
