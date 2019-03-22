import pandas as pd
from scipy.interpolate.interpolate import interp1d


class ExternalBase(object):

    def __init__(self, path, col_num):

        df = pd.read_csv(path, index_col=0, parse_dates=True)
        df['delta t'] = df.index.to_series().diff().dt.total_seconds()
        df['delta t'].iloc[0] = 0
        x_range = df['delta t'].cumsum().tolist()
        y_range = df.iloc[:, col_num].tolist()

        # added to allow multi-year simulations
        self.max_time = 0
        x_range.append(x_range[-1] + (x_range[-1] - x_range[-2]))
        y_range.append(y_range[0])
        self.max_time = x_range[-1]

        self._interp_values = interp1d(x_range, y_range)

    def get_value(self, time):
        return float(self._interp_values(time % self.max_time))
