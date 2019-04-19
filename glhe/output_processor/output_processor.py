import datetime as dt
import os
from os.path import join, normpath

import pandas as pd


class OutputProcessor(object):

    def __init__(self, output_dir: str, output_name: str) -> None:
        """
        Output processor manages output data
        """

        self.output_dir = output_dir
        self.output_file = output_name
        self.write_path = normpath(join(output_dir, output_name))
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

        self.convert_time_to_timestamp()
        self.df.to_csv(self.write_path)

    def convert_time_to_timestamp(self) -> None:
        """"
        Convert the 'Elapsed Time' column to a standardized date/time format.
        """
        try:
            dts = [dt.timedelta(seconds=x) for x in self.df['Elapsed Time [s]'].values.tolist()]
            start_time = dt.datetime(year=dt.datetime.now().year, month=1, day=1, hour=0, minute=0)
            time_stamps = [start_time + x for x in dts]
            self.df['Date/Time'] = time_stamps
            self.df.set_index('Date/Time', inplace=True)
        except KeyError:
            pass
