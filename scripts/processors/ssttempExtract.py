from netCDF4 import *
from config import *

# VALIDATES THAT ALL DATA EXISTS FOR the sets above and extracts temp into a single set

# converts day into string
def daycalc(day):
    day = str(day)
    while (len(day) < 3):
        day = "0" + day
    return day

#outputs yy mm dd format
def dateformat(year, day):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month = 1
    if (year % 4 == 0):
        day -= 1
    while (days[month - 1] < day):
        day -= days[month - 1]
        month += 1
    return str(year) + "," + str(month) + "," + str(day)

def validator(year, day):
    global out
    day = daycalc(day)
    filelocation = DIRECTORY + f'/data/raw/sst/sst_{year}_{day}.nc'

    dataset = Dataset(filelocation, "r", format="NETCDF4")

    out += str(dateformat(int(year), int(day))) + "," + str(dataset.variables["sst"][0][set[0]][set[1]]) + "\n"
    dataset.close()


for set in sets.values():
    outlocation = DIRECTORY + f'/data/processed/sst/{set[0]}_{set[1]}.txt'
    out = "YY,MM,DD,WTMP\n"
    for year in range(2012, 2024):
        print(year)
        modifier = 0
        if (year % 4 == 0):
            modifier = 1
        for day in range(152 + modifier, 305 + modifier):
            validator(year, day)
    output = open(outlocation, "w")
    output.write(out)
    output.close()
