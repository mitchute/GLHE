import os

import pandas as pd


class OutputProcessor(object):

    def __init__(self):
        # self.output_vars_data = {}
        self.df = pd.DataFrame()
        self.idx_count = 0

    def collect_output(self, data_to_collect):

        temp_dict = {}
        for data in data_to_collect:
            for key, val in data.items():
                temp_dict[key] = val

        df_temp = pd.DataFrame(temp_dict, index=[self.idx_count])
        self.df = pd.concat([self.df, df_temp], axis=0, sort=True)
        self.idx_count += 1

    def write_to_file(self, path):
        # write the data to a file
        if os.path.exists(path):
            os.remove(path)

        with open(path, 'w') as f:  # pragma: no cover
            self.df.to_csv(f)  # pragma: no cover
            f.close()  # pragma: no cover
