import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
from config import DIRECTORY
matplotlib.use('TkAgg')




buoy = "dulm5"
sst = [563,23]
buoylocation = DIRECTORY + f"/processor/processedData/alldata/{buoy}.txt"
sstlocation = DIRECTORY + f'/processor/processedData/alldata/{sst[0]}_{sst[1]}.txt'

buoyin = open(buoylocation, "r")
sstin = open(sstlocation, "r")

buoylines = buoyin.readlines()
sstlines = sstin.readlines()

buoydata = [line[:-1] for line in buoylines]
sstdata = [line[:-1] for line in sstlines]
print(len(buoydata), len(sstdata))
for line in range (len(buoydata)):
    try:
        buoydata[line] = float(buoydata[line])
    except:
        buoydata[line] = np.nan
    try:
        sstdata[line] = float(sstdata[line])
    except:
        sstdata[line] = np.nan
print(len(buoydata), len(sstdata))
plt.plot(buoydata, color = "royalblue")
plt.plot(sstdata, color = "orange")
plt.show()



