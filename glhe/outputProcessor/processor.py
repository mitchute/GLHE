import pandas as pd


class OutputProcessor(object):
    # Class-level variables to store output data
    output_vars_data = {}
    df = pd.DataFrame()
    idx_count = 0

    def __init__(self):
        # nothing to init
        pass

    def register_output_variable(self, inst, attr, key):
        # registers and output variable with the output processor.py
        OutputProcessor.output_vars_data[key] = (inst, attr)

    def report_output(self, index=None):
        if index == None:
            index = OutputProcessor.idx_count

        # adds another row to the output data dataframe
        temp_dict = {}
        for key, spec in self.output_vars_data.items():
            temp_dict[key] = getattr(*spec)

        df_temp = pd.DataFrame(temp_dict, index=[index])
        OutputProcessor.df = pd.concat([OutputProcessor().df, df_temp], axis=0)
        OutputProcessor.idx_count += 1

    def write_to_file(self, path):
        # write the data to a file
        OutputProcessor.df.to_csv(path)  # pragma: no cover


op = OutputProcessor()
