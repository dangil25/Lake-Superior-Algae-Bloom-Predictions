import requests
import os
from netCDF4 import *
from datetime import *
from math import *
from config import DIRECTORY

set = [566, 42]
#corresponding coordinates
coords = [46.8077700019549, -91.8312990064853]

#VALIDATES THAT ALL DATA EXISTS FOR the sets above and extracts temp into a single set

def daycalc (day):
    day = str(day)
    while (len(day) < 3):
        day = "0" + day
    return day

outlocation = DIRECTORY + f'/processor/processedData/alldata/{set[0]}_{set[1]}.txt'

out = ""

def validator(year, day):
    global out
    day = daycalc(day)
    filelocation = DIRECTORY  + f'/processor/data/sst/sst_{year}_{day}.nc'

    dataset = Dataset(filelocation, "r", format="NETCDF4")

    lats = dataset.variables["lat"]
    longs = dataset.variables["lon"]
    realset = [0, 0]

    for i in range (len(lats)):
        if (coords[0] == lats[i]):
            realset[0] = i
            break

    for j in range (len(longs)):
        if (coords[1] == longs[j]):
            realset[1] = j
            break
    # tests if data is missing/empty/at different index
    if (realset[0] == 0 or realset[1] == 0): print(year, day, "doesn't exist")
    elif (realset[0] != set[0] and realset[1] != set[1]): print(year, day, "diff index")
    elif (dataset.variables["sst"][0][set[0]][set[1]] == 999): print(year, day, "999")
    else: out += str(dataset.variables["sst"][0][set[0]][set[1]]) + "\n"
    dataset.close()

for year in range (2012, 2024):
    modifier = 0
    if (year % 4 == 0):
        modifier = 1
    for day in range(152 + modifier, 305 + modifier):
        try:
            validator(year, day)

        except:
            pass
output = open(outlocation, "w")
output.write(out)
output.close()
