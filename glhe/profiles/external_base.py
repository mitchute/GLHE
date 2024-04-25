from pathlib import Path

import csv
from datetime import datetime
from glhe.utilities.functions import Interpolator1D


class ExternalBase(object):

    def __init__(self, path: Path, col_num: int):
        x_range, y_range = self.read_csv_and_compute_delta_t(path, col_num)
        # added to allow multi-year simulations
        self.max_time = 0
        self.max_time = x_range[-1]
        self._interp_values = Interpolator1D(x_range, y_range)

    @staticmethod
    def read_csv_and_compute_delta_t(file_path: Path, col_num: int) -> [list, list]:
        delta_t_values = []
        y_values = []
        last_timestamp = None

        # Open CSV file and read data
        with file_path.open('r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Read header

            for row in csvreader:
                timestamp_str = row[0]

                # Convert timestamp string to datetime object
                current_timestamp = None
                time_stamp_formats = ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M', '%m/%d/%Y %H:%M:%S']
                for t in time_stamp_formats:
                    try:
                        current_timestamp = datetime.strptime(timestamp_str, t)
                        break
                    except ValueError:
                        continue
                if not current_timestamp:
                    raise ValueError(f"Bad timestamp format for timestamp: {timestamp_str}")

                if last_timestamp is not None:
                    # Calculate delta t in seconds
                    delta_t = (current_timestamp - last_timestamp).total_seconds()
                    delta_t_values.append(delta_t)

                # Append value to y_values
                y_values.append(row[col_num + 1])

                last_timestamp = current_timestamp

        # Initialize x_range with cumulative sum of delta_t_values
        x_range = [0]
        cumulative_sum = 0
        for delta_t in delta_t_values:
            cumulative_sum += delta_t
            x_range.append(cumulative_sum)

        # Append an extrapolated value to x_range
        x_range.append(x_range[-1] + (x_range[-1] - x_range[-2]))

        # Append the first y_value to y_range
        y_values.append(y_values[0])

        return x_range, y_values

    def get_value(self, time) -> float:
        return float(self._interp_values.interpolate(time % self.max_time))
