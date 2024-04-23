import datetime as dt
from pathlib import Path


class OutputProcessor:

    def __init__(self, output_dir: Path, output_name: str):
        """
        Output processor manages output data
        """

        self.output_dir = output_dir
        self.output_file = output_name
        self.write_path = output_dir / output_name
        # self.df = pd.DataFrame()
        self.output_data = []
        self.idx_count = 0

    def collect_output(self, data_dict: dict) -> None:
        """
        Collect output data and log it in a DataFrame until it's written to a file.

        :param data_dict: dictionary of data to be logged
        """
        self.output_data.append(data_dict)
        # df_temp = pd.DataFrame(data_dict, index=[self.idx_count])
        # self.df = pd.concat([self.df, df_temp], axis=0, sort=True)
        # self.idx_count += 1

    def write_to_file(self) -> None:
        """
        Write the DataFrame holding the simulation data to a file.
        """
        if self.write_path.exists():
            self.write_path.unlink()

        header_row = ['Date/Time']
        header_row.extend([key for key in sorted(self.output_data[0].keys()) if key != 'Elapsed Time [s]'])

        time_stamps = self.convert_time_to_timestamp()
        with self.write_path.open('w') as f:
            for i, d in enumerate(self.output_data):
                if i == 0:
                    f.write(','.join(header_row) + '\n')
                row = [time_stamps[i]]
                sorted_values_without_time = [str(d[key]) for key in sorted(d.keys()) if key != 'Elapsed Time [s]']
                row.extend(sorted_values_without_time)
                f.write(','.join(row) + '\n')

    def convert_time_to_timestamp(self) -> list[str]:
        """
        Convert the 'Elapsed Time' column to a standardized date/time format.
        """
        try:
            raw_dts = [d['Elapsed Time [s]'] for d in self.output_data]
            dts = [dt.timedelta(seconds=x) for x in raw_dts]
            start_time = dt.datetime(year=dt.datetime.now().year, month=1, day=1, hour=0, minute=0)
            time_stamps = [str(start_time + x) for x in dts]
            return time_stamps
        except KeyError:
            pass
