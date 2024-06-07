import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import KNNImputer
from sklearn.impute import IterativeImputer
import matplotlib as mpl
from config import DIRECTORY

#Creates and imputes any missing buoy data

buoy = "45028"


#processed buoy data for corresponding location
buoylocation = DIRECTORY + f'/processor/data/buoy/{buoy}/daily.xlsx'
truncfill = DIRECTORY + f'/processor/data/buoy/{buoy}/truncfill.xlsx'
fullfill = DIRECTORY + f'/processor/data/buoy/{buoy}/fullfill.xlsx'

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

#imputes partially missing data
def truncatedImputer(df):

    df['#YY'] = df['#YY']*365
    df['MM'] = df['MM'] * 30
    iter_imputer = IterativeImputer(missing_values=np.nan, max_iter = 100, random_state=42)
    iter_imputed = iter_imputer.fit_transform(df)
    iter_imputed = pd.DataFrame(iter_imputed, columns=df.columns)

    iter_imputed['#YY'] = iter_imputed['#YY']//365
    iter_imputed['MM'] = iter_imputed['MM']//30
    return iter_imputed

#imputes any completely missing rows
def filledImputer(df):
    #creates weighing for dates
    df['#YY'] = df['#YY']*365
    df['MM'] = df['MM'] * 30
    # knn_imputer = KNNImputer(missing_values = np.nan, n_neighbors = 30)
    # knn_imputed = knn_imputer.fit_transform(df)
    # knn_imputed = pd.DataFrame(knn_imputed, columns = df.columns)
    # knn_imputed['#YY'] = knn_imputed['#YY']//365
    # knn_imputed['MM'] = knn_imputed['MM']//30
    # return knn_imputed
    iter_imputer = IterativeImputer(missing_values=np.nan, max_iter = 10, random_state=42)
    knn_imputed = iter_imputer.fit_transform(df)
    knn_imputed = pd.DataFrame(knn_imputed, columns = df.columns)
    knn_imputed['#YY'] = knn_imputed['#YY']//365
    knn_imputed['MM'] = knn_imputed['MM']//30
    return knn_imputed

#isolates buoy data from june 1st to october 31st
def cleaner(df):
    df = df[df['MM'] < 11]
    df = df[df['MM'] > 5]
    df = df.reset_index(drop = True)
    df = truncatedImputer(df)
    return df

#adds any missing rows (empty)
#CALL TRUNCATED IMPUTER FIRST
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
    df.reset_index(drop = True)
    return df


def main():
    df = pd.read_excel(buoylocation, sheet_name='daily')
    #truncates to necessary dates and imputes missing data
    df = cleaner(df)
    df = createMissing(df)
    df.to_excel(truncfill, index=False, sheet_name='truncfill')
    #creates rows and imputes for any missing days
    df = filledImputer(df)
    df.to_excel(fullfill, index=False, sheet_name='fullfill')


main()
