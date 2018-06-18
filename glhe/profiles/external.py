import os

import pandas as pd
from scipy.interpolate.interpolate import interp1d

from glhe.profiles.base import Base


class External(Base):

    def __init__(self, path):
        Base.__init__(self)

        path = os.path.normpath(os.path.join(os.getcwd(), path))

        df = pd.read_csv(path, index_col=0, parse_dates=True)
        delta_t = df.index.to_series().diff().dt.total_seconds()
        delta_t.is_copy = False
        delta_t[0] = 0
        x_range = delta_t.cumsum().tolist()
        self._max_time = x_range[-1]
        y_vals = df.iloc[:, 0].tolist()
        self._interp_values = interp1d(x_range, y_vals)

    def get_value(self, time=0):
        return self._interp_values(time % self._max_time)
