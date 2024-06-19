from netCDF4 import *
from math import *

from processor.config import DIRECTORY

#This finds and returns all satellite temp points within limit miles of location
#The output is formatted: lat, long, lat index, long index, distance


#Location
group = 4
location = [48.133107, -88.929242]
#Max distance to location
limit = 1


def daycalc (day):
    #returns three digit string of day
    day = str(day)
    while (len(day) < 3):
        day = "0" + day
    return day

def distance (l1, l2):
    #finds the difference between two given sets of coordinates (lat, lon) in miles
    #[lat, lon]
    lon1 = radians(l1[1])
    lon2 = radians(l2[1])
    lat1= radians(l1[0])
    lat2 = radians(l2[0])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371/1.60937

    # calculate the result
    return (c * r)

def extractfile(year, day):
    day = daycalc(day)

    filelocation = DIRECTORY + f'/data/raw/sst/sst_{year}_{day}.nc'

    dataset = Dataset(filelocation, "r", format = "NETCDF4")
    lats = dataset.variables["lat"]
    longs = dataset.variables["lon"]
    #time, lats, longs

    outlocation = DIRECTORY + f'/data/processed/distance/distance_output_{group}.txt'
    output = open(outlocation, "w")

    valid = ""
    close = []
    #finds all sets of coordinates within limit to location
    for lat in range (len(lats)):
        if (not (distance(location, [lats[lat], location[1]]) < limit)):
             continue
        for long in range (len(longs)):
            if (distance(location, [lats[lat], longs[long]]) < limit):
                close.append([lat, long])
    #adds each set from above into a txt
    for set in close:
        valid += (str(lats[set[0]]) + "," + str(longs[set[1]]) + " " + str(set[0]) + "," + str(set[1]) + " " +
                str(distance(location, [lats[set[0]], longs[set[1]]])) + "\n")

    valid += ""
    output.write(valid)
    output.close()
    dataset.close()

#extracts for a specific date, but it seems that all indexes and coords are the same for all days.
extractfile(2012, 153)
