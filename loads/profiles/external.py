import os

import numpy as np
from scipy.interpolate.interpolate import interp1d

from loads.profiles.base import Base


class External(Base):

    def __init__(self, path):
        Base.__init__(self)

        path = os.path.normpath(os.path.join(os.getcwd(), path))

        # noinspection PyTypeChecker
        self.values = np.genfromtxt(path, delimiter=',', skip_header=1, usecols=1)
        x_range = np.arange(len(self.values)) * 3600
        self._max_time = x_range[-1]
        self._interp_values = interp1d(x_range, self.values)

    def get_value(self, time=0):

        if time <= self._max_time:
            return self._interp_values(time)
        else:
            return self._interp_values(time % self._max_time)
