import os
from os.path import join, normpath

import pandas as pd


class OutputProcessor(object):

    def __init__(self, output_path: str, output_name: str) -> None:
        """
        Output processor manages output data
        """

        self.write_path = normpath(join(output_path, output_name))
        self.df = pd.DataFrame()
        self.idx_count = 0

    def collect_output(self, data_dict: dict) -> None:
        """
        Collect output data and log it in a DataFrame until it's written to a file.

        :param data_dict: dictionary of data to be logged
        """

        df_temp = pd.DataFrame(data_dict, index=[self.idx_count])
        self.df = pd.concat([self.df, df_temp], axis=0, sort=True)
        self.idx_count += 1

    def write_to_file(self) -> None:
        """
        Write the DataFrame holding the simulation data to a file.
        """
        if os.path.exists(self.write_path):
            os.remove(self.write_path)

        with open(self.write_path, 'w') as f:  # pragma: no cover
            self.df.to_csv(f)  # pragma: no cover
            f.close()  # pragma: no cover
