from config import *
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pandas.plotting import autocorrelation_plot
from pandas.plotting import lag_plot

matplotlib.use('TkAgg')

df = pd.read_csv(f"{DIRECTORY}/data/final/group_3.txt")
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')
# plt.plot(df["ATMP"], label="ATMP")
# plt.plot(df["WTMP"], label="WTMP")
# plt.plot(df["WSPD"], label="WSPD")
# plt.plot(df["WDIR"], label="WDIR")
# plt.plot(df["DISC"]/100, label="DISC")
df = df.dropna()
#a = autocorrelation_plot(df['2012':'2023']['ATMP'])
a = lag_plot(df['2012':'2023']['DISC'], lag=1)
a.plot()
plt.show()