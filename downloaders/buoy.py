import numpy as np
import pandas as pd
import requests
import os
import re
from config import DIRECTORY

#this takes all the data for a specific buoy and converts into a daily average from 2012 - 2023
buoy = "sxhw3"


def download():

    #downloads all data for this buoy
    for year in range(2012, 2023): downloadall(year)
    download2023()

def downloadall(year):
    #downloads yearly data from 2012-2022
    folder = DIRECTORY + 'processor/data/buoy/{buoy}'
    #create folder
    if (not os.path.isdir(folder)):
        os.makedirs(folder)
    #download
    path = DIRECTORY + f'/processor/data/buoy/{buoy}/{year}.txt'
    if (not os.path.isfile(path)):
        url = f'https://www.ndbc.noaa.gov/view_text_file.php?filename={buoy}h{year}.txt.gz&dir=data/historical/stdmet/'
        print(url)
        req = requests.get(url, allow_redirects=True)
        open(path, 'wb').write(req.content)
    else: print(path + " already exists")
def download2023():
    #downloads monthly data for 2023
    year = 2023
    folder = DIRECTORY + f'/processor/data/buoy/{buoy}'
    # create folder
    if (not os.path.isdir(folder)):
        os.makedirs(folder)
    # download
    for month in range (6, 10):
        path = DIRECTORY + f'/processor/data/buoy/{buoy}/{year}{month}.txt'
        if (not os.path.isfile(path)):
            monthname = ['Jun', 'Jul', 'Aug', 'Sep'][month - 6]
            url = f'https://www.ndbc.noaa.gov/view_text_file.php?filename={buoy}{month}{year}.txt.gz&dir=data/stdmet/{monthname}/'
            print(url)
            req = requests.get(url, allow_redirects=True)
            open(path, 'wb').write(req.content)
    #NOAA is annoying and can't standardize URLS, so this is for october data:
    for month in range (10, 11):
        path = DIRECTORY + f'/processor/data/buoy/{buoy}/{year}{month}.txt'
        if (not os.path.isfile(path)):
            url = f'https://www.ndbc.noaa.gov/data/stdmet/Oct/{buoy}.txt'
            print(url)
            req = requests.get(url, allow_redirects=True)
            open(path, 'wb').write(req.content)
def tocsv():
    #read and combines data into a single csv file
    data = []
    for year in range (2012, 2023):
        path = DIRECTORY + f'/processor/data/buoy/{buoy}/{year}.txt'
        #open and read by line
        txt = open(path, 'r')
        lines = [line.rstrip() for line in txt]

        #add header
        if (year == 2012):
            data.append(re.split(' +', lines[0]))

        #add line by line to data
        for i in range(2, len(lines)):
            data.append(re.split(' +', lines[i]))

    #monthly data for 2023
    for year in range (2023, 2024):
        for month in range (6, 11):
            path = DIRECTORY + f'/processor/data/buoy/{buoy}/{year}{month}.txt'
            # open and read by line
            txt = open(path, 'r')
            lines = [line.rstrip() for line in txt]

            # add line by line to data
            for i in range(2, len(lines)):
                data.append(re.split(' +', lines[i]))

    df = pd.DataFrame(data[1::], columns =data[0])
    df.apply(pd.to_numeric)
    path = DIRECTORY + f'/processor/data/buoy/{buoy}/alldata.xlsx'
    print(1)
    df.to_excel(path, index=False, sheet_name = 'alldata')
    return df

def toDay():
    #takes all data and combines it into daily averages
    inpath = DIRECTORY + f'/processor/data/buoy/{buoy}/alldata.xlsx'
    outpath = DIRECTORY + f'/processor/data/buoy/{buoy}/daily.xlsx'

    df = pd.read_excel(inpath, sheet_name='alldata')
    df = df.drop(columns = ['GST', 'WVHT', 'DPD', 'MWD', 'VIS', 'TIDE', 'APD', 'hh', 'mm'])
    df = df.replace([9999, 999, 99, ''], np.nan)
    y = df.groupby(["#YY", "MM", "DD"], as_index=False).mean()
    y.to_excel(outpath, index = False, sheet_name = 'daily')

download()
tocsv()
toDay()
