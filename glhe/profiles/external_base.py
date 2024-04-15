from pathlib import Path

import pandas as pd

from glhe.utilities.functions import Interpolator1D


class ExternalBase(object):

    def __init__(self, path: Path, col_num: int):

        df = pd.read_csv(str(path), index_col=0, parse_dates=True)
        df['delta t'] = df.index.to_series().diff().dt.total_seconds()
        df['delta t'].iat[0] = 0
        x_range = df['delta t'].cumsum().tolist()
        y_range = df.iloc[:, col_num].tolist()

        # added to allow multi-year simulations
        self.max_time = 0
        x_range.append(x_range[-1] + (x_range[-1] - x_range[-2]))
        y_range.append(y_range[0])
        self.max_time = x_range[-1]

        self._interp_values = Interpolator1D(x_range, y_range)

    def get_value(self, time) -> float:
        return float(self._interp_values.interpolate(time % self.max_time))
