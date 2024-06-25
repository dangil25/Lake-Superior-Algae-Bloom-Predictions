import pandas as pd
import matplotlib
from config import *
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

group = 3
df = pd.read_csv(f"{DIRECTORY}/data/final/group_{group}.txt")
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

plt.plot(df["ATMP"], label="ATMP")
plt.plot(df["WTMP"], label="WTMP")
plt.plot(df["WSPD"], label="WSPD")
plt.plot(df["DISC"], label="DISC")
plt.legend(loc="upper right")
for bloom in blooms[group]:
    plt.axvline(x=pd.to_datetime(f"{bloom[0]}-{bloom[1]}-{bloom[2]}"), color="grey")
plt.show()
