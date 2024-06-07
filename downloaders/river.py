import requests
import os
from config import *

#date format 2012-01-01
#date range to download
begindate = "2012-01-01"
enddate = "2023-08-31"


codes = {"discharge" : "00060"}
dayinmonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def inrange(date):
    print(date[0])
    day = int(date[2])
    for i in range (int(date[1]) - 1):
        day += dayinmonth[i]
    if (152 <= day and day < 305):
        return True
    return False

def download():
    for river in rivernames:
        id = riverids[river]
        for codename in codes:
            path = DIRECTORY + f'/processor/data/river/{codename}_{river}.txt'
            if (not os.path.isfile(path)):
                print(path)
            url = f"https://waterdata.usgs.gov/nwis/dv?cb_{codes[codename]}=on&format=rdb&site_no={id}&legacy=&referred_module=sw&period=&begin_date={begindate}&end_date={enddate}"
            print(url)
            req = requests.get(url, allow_redirects=True)
            open(path, 'wb').write(req.content)





def main():
    download()
main()