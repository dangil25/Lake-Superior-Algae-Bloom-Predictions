import matplotlib.pyplot as plt
import matplotlib
from config import *
matplotlib.use('TkAgg')
river1 = rivernames[3]
river2 = rivernames[4]
dischargelocation1 = DIRECTORY + f"/data/processed/river/discharge_{river1}_final.txt"
dischargelocation2 = DIRECTORY + f"/data/processed/river/discharge_{river2}_final.txt"

dischargein1 = open(dischargelocation1, "r")
dischargein2 = open(dischargelocation2, "r")

dischargelines1 = dischargein1.readlines()[1:]
dischargelines2 = dischargein2.readlines()[1:]
dischargedata1 = [float(line.split(",")[3]) for line in dischargelines1]
dischargedata2 = [float(line.split(",")[3]) for line in dischargelines2]

plt.plot(dischargedata1, color = "royalblue")
plt.plot(dischargedata2, color = "orange")
plt.show()