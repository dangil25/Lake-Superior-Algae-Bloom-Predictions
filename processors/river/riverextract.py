from processor.config import *

codes = {"discharge": "00060"}
dayinmonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def inrange(date):
    day = int(date[2])
    for i in range(int(date[1]) - 1):
        day += dayinmonth[i]
    if (152 <= day and day < 305):
        return True
    return False


def dischargedata():
    for river in rivernames:
        try:
            codename = "discharge"
            inpath = DIRECTORY + f'/processor/data/river/{codename}_{river}.txt'
            outpath = DIRECTORY + f'/processor/processedData/river/{codename}_{river}_final.txt'
            file = open(inpath, "r")
            out = "YY MM DD DISC \n"
            for line in file:
                if (line[0:4] == "USGS"):
                    l = line.split("\t")
                    date = l[2]
                    procdate = date.split('-')[0] + " " + date.split('-')[1] + " " + date.split('-')[2]
                    if (inrange(date.split("-"))):
                        meandischarge = l[3]
                        out += procdate + " " + meandischarge + "\n"
            file.close()
            open(outpath, 'w').write(out)
        except:
            pass


dischargedata()
