import os

import pandas as pd


class OutputProcessor(object):

    def __init__(self):
        """
        Output processor manages output data
        """
        self.df = pd.DataFrame()
        self.idx_count = 0

    def collect_output(self, data_dict: dict) -> None:
        """
        Collect output data and log it in a DataFrame until it's written to a file.

        :param data_dict:
        :return: None
        """
        temp_dict = {}
        for data in data_dict:
            for key, val in data.items():
                temp_dict[key] = val

        df_temp = pd.DataFrame(temp_dict, index=[self.idx_count])
        self.df = pd.concat([self.df, df_temp], axis=0, sort=True)
        self.idx_count += 1

    def write_to_file(self, write_path: str) -> None:
        """
        Write the DataFrame holding the simulation data to a file.

        :param write_path:
        :return:
        """
        if os.path.exists(write_path):
            os.remove(write_path)

        with open(write_path, 'w') as f:  # pragma: no cover
            self.df.to_csv(f)  # pragma: no cover
            f.close()  # pragma: no cover
