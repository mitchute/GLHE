import pandas as pd
from scipy.interpolate.interpolate import interp1d

from glhe.profiles.base import Base


class ExternalLoad(Base):

    def __init__(self, path):
        Base.__init__(self)

        df = pd.read_csv(path, index_col=0, parse_dates=True)
        delta_t = df.index.to_series().diff().dt.total_seconds()
        delta_t.is_copy = False
        delta_t[0] = 0
        x_range = delta_t.cumsum().tolist()
        y_range = df.iloc[:, 0].tolist()
        self._interp_values = interp1d(x_range, y_range)

    def get_value(self, time):
        return self._interp_values(time)
