import numpy as np
import pandas as pd
from config import DIRECTORY

#fill all empty rows with np.nan for good graphing
buoy = 45028

buoylocation = DIRECTORY + f'/processor/data/buoy/{buoy}/daily.xlsx'
emptyfill = DIRECTORY + f'/processor/data/buoy/{buoy}/emptyfill.xlsx'

#calculates month
def monthcalc (year, day):
    #Returns two-digit string of month
    if (year % 4 == 0): days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else: days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sum = month = 0
    while (sum < day):
        sum += days[month]
        month += 1
    return month

#calculates day in month
def daycalc(year, month, day):
    days = [31, 28 + (year % 4 == 0), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    counter = 0
    for m in range (month - 1):
        counter += days[m]
    out = 0
    while(counter != day):
        out += 1
        counter += 1
    return out

#calculate previous day to get index from which to insert
def previous(year, month, day):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (day == 1):
        if (month == 6):
            year -= 1
            month = 10
        else:
            month -= 1
        day = days[month - 1]
    else:
        day -= 1
    return [year, month, day]

def cleaner():
    df = pd.read_excel(buoylocation, sheet_name='daily')
    df = df[df['MM'] < 11]
    df = df[df['MM'] > 5]
    return df


def createMissing(df):
    print(df.keys())
    for year in range (2012, 2024):
        modifier = 0
        if (year % 4 == 0):
            modifier = 1
        for day in range(152 + modifier, 305 + modifier):
            month = monthcalc(year, day)
            realday = daycalc(year, month, day)
            if (not ((df['#YY'] == year) & (df['MM'] == monthcalc(year, day)) & (df['DD'] == realday)).any()):
                arr = previous(year, month, realday)
                print(arr[0], arr[1], arr[2])
                index = df.loc[(df['#YY'] == arr[0]) & (df['MM'] == arr[1]) & (df['DD'] == arr[2])].index
                df = pd.DataFrame(np.insert(df.values, index + 1, values = [year, month, realday, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], axis = 0), columns = df.columns)
    df.to_excel(emptyfill, index = False, sheet_name = 'emptyfill')

df = cleaner()
createMissing(df)
