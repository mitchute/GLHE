import datetime

import numpy as np
import pandas as pd

ghe_length = 76.2

heat = np.concatenate((np.ones([180]) * (25 * ghe_length),
                       np.ones([180]) * (50 * ghe_length) ,
                       np.ones([180]) * (25 * ghe_length),
                       np.ones([180]) * (0 * ghe_length),
                       np.ones([180]) * (-25 * ghe_length),
                       np.ones([180]) * (-50 * ghe_length),
                       np.ones([180]) * (-25 * ghe_length),
                       np.ones([180]) * (0 * ghe_length),
                       np.ones([180]) * (25 * ghe_length)), axis=0)
start_time = datetime.datetime(month=1, day=1, year=2018, hour=0, minute=0, second=0)
times = pd.date_range(start_time, start_time + datetime.timedelta(minutes=(len(heat) - 1)), freq='T')
m_dot = np.ones([len(heat)]) * 0.2
df = pd.DataFrame({"Date/Time": times, "Total Power [W]": heat, "mdot [kg/s]": m_dot})
df = df.set_index("Date/Time")
df.to_csv("MHR_loads.csv")
