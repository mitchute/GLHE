import os

import pandas as pd


class OutputProcessor(object):

    def __init__(self):
        self.output_vars_data = {}
        self.df = pd.DataFrame()
        self.idx_count = 0

    def register_output_variable(self, inst, attr, key):
        # registers and output variable with the output processor.py
        self.output_vars_data[key] = (inst, attr)

    def report_output(self, index=None):
        if index is None:
            index = self.idx_count

        # adds another row to the output data dataframe
        temp_dict = {}
        for key, spec in self.output_vars_data.items():
            temp_dict[key] = getattr(*spec)

        df_temp = pd.DataFrame(temp_dict, index=[index])
        self.df = pd.concat([self.df, df_temp], axis=0, sort=True)
        self.idx_count += 1

    def write_to_file(self, path):
        # write the data to a file
        if os.path.exists(path):
            os.remove(path)

        with open(path, 'w') as f:  # pragma: no cover
            self.df.to_csv(f)  # pragma: no cover
            f.close()  # pragma: no cover


op = OutputProcessor()
