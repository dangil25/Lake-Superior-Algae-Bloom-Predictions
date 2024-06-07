import numpy as np
import pandas as pd
from processor.config import *
pd.options.mode.chained_assignment = None

days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def to_day(df, year, month, day):
    #year, month, day, windir, winspd, airtemp
    output = [int(year), int(month), int(day), 0, 0, 0]
    #isolates needed day
    df_new = df.loc[(df['YY'] == year) & (df['MM'] == month) & (df['DD'] == day)]
    #consolidates wspd and air temperature
    output[4] = round(df_new['WSPD'].mean(), 2)
    output[5] = round(df_new['ATMP'].median(), 2)
    #WDIR into 8 directions, converts it into nparray to get counts of each direction, and take one that
    # occurs most often. Determined that this is okay as >70% of all wind is +- 45 degrees of this direction
    try:
        df_new['WDIR'] = (df_new['WDIR'] + 22.5)//45 % 8
        wdirs = np.array(df_new['WDIR'].loc[df_new['WDIR'].notna()], dtype=int)
        output[3] = np.bincount(wdirs).argmax()
    except:
        output[3] = np.nan
    return output


for buoyid in buoyids:
    print(buoyid)
    inppath = f"{DIRECTORY}/processor/data/buoy/{buoyid}_raw.txt"
    outpath = f"{DIRECTORY}/processor/processedData/buoy/{buoyid}_final.txt"
    df = pd.read_csv(inppath, sep=',')
    df = df[df['MM'] < 11]
    df = df[df['MM'] > 5]
    df = df.reset_index(drop=True)
    df_out = pd.DataFrame(columns=['YY', 'MM', 'DD', 'WDIR', 'WSPD', 'ATMP'])
    for year in range (2012, 2024):
        for month in range (6, 11):
            for day in range (1, days[month - 1] + 1):
                output = to_day(df, year, month, day)
                df_out.loc[len(df_out.index)] = output
    df_out.to_csv(outpath, index=False)


