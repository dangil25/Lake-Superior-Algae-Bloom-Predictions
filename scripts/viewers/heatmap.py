import pandas as pd
from config import DIRECTORY
import seaborn as sn
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

df = pd.read_csv(f"{DIRECTORY}/data/final/group_1.txt")
df = df.drop(columns=["date"])
hm = sn.heatmap(data=df.corr(), cmap="RdYlGn", square=True)
plt.show()

