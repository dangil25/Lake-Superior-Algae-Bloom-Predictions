import matplotlib.pyplot as plt
import matplotlib
from processor.config import *
matplotlib.use('TkAgg')
river = rivernames[1]
dischargelocation = DIRECTORY + f"/processor/processedData/river/discharge_{river}_final.txt"

dischargein = open(dischargelocation, "r")

dischargelines = dischargein.readlines()

dischargedata = [float(line.split(" ")[1]) for line in dischargelines]
print(dischargedata)
print(len(dischargedata))

plt.plot(dischargedata)
plt.show()