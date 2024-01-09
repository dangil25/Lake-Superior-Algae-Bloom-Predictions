import requests
import os
from datetime import *
from math import *
from config import DIRECTORY

#long, lat
from netCDF4 import *
def monthcalc (year, day):
    #Returns two-digit string of month
    if (year % 4 == 0): days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else: days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = int(day)
    sum = 0
    month = 0
    while (sum < day):
        sum += days[month]
        month += 1
    month = str(month)
    if (len(month) == 1): month = "0" + month
    return month

def daycalc (day):
    #returns three digit string of day
    day = str(day)
    while (len(day) < 3):
        day = "0" + day
    return day



def download(year, day):
    #Downloads the relevant nc file
    path = DIRECTORY + f'/processor/data/sst/sst_{year}_{day}.nc'
    #Checks if file is already downloaded
    if (not os.path.isfile(path)):
        print(path)
        month = monthcalc(year, day)
        url = f'https://apps.glerl.noaa.gov/thredds/fileServer/glsea_nc_3/{year}/{month}/{year}_{day}_glsea_sst.nc'
        req = requests.get(url, allow_redirects=True)

        open(path,'wb').write(req.content)

def delete(year, day):
    #Deletes the relevant nc file
    #commented out for safety
    # path = DIRECTORY + f'/processor/data/sst/sst_{year}_{day}.nc'
    # os.remove(path)
    return 0

for year in range (2012, 2024):
    #leap year modifier
    modifier = 0
    if (year % 4 == 0):
        modifier = 1
    for day in range(152 + modifier, 305 + modifier):
        print(year, day)
        download(year, day)







