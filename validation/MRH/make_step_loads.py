import datetime

import numpy as np
import pandas as pd

heat = np.concatenate((np.ones([60]) * 2500,
                       np.ones([60]) * 5000,
                       np.ones([60]) * 2500,
                       np.ones([60]) * 1250,
                       np.ones([60]) * 2500), axis=0)
start_time = datetime.datetime(month=1, day=1, year=2018, hour=0, minute=0, second=0)
times = pd.date_range(start_time, start_time + datetime.timedelta(minutes=299), freq='T')
m_dot = np.ones([300]) * 0.2
df = pd.DataFrame({"Date/Time": times, "Total Power [W]": heat, "mdot [kg/s]": m_dot})
df = df.set_index("Date/Time")
df.to_csv("MHR.csv")
