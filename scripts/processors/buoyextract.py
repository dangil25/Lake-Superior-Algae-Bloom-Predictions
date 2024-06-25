import numpy as np
import pandas as pd
from config import *
from math import sin, cos, pi
pd.options.mode.chained_assignment = None

days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def to_day(df, year, month, day):
    #year, month, day, windir, winspd, airtemp
    output = [int(year), int(month), int(day), 0, 0, 0, 0]
    #isolates needed day
    df_new = df.loc[(df['YY'] == year) & (df['MM'] == month) & (df['DD'] == day)]

    # consolidates wspd and air temperature
    output[5] = round(df_new['WSPD'].mean(), 2)
    output[6] = round(df_new['ATMP'].median(), 2)

    #WDIR into 8 directions, converts it into nparray to get counts of each direction, and take one that
    # occurs most often. Determined that this is okay as >70% of all wind is +- 45 degrees of this direction
    try:
        df_new['WDIR'] = (df_new['WDIR'] + 22.5)//45 % 8
        wdirs = np.array(df_new['WDIR'].loc[df_new['WDIR'].notna()], dtype=int)
        dir = int(np.bincount(wdirs).argmax())
        output[3] = round(cos(dir * 2 * pi / 8), 2)
        output[4] = round(sin(dir * 2 * pi / 8), 2)

    except:
        output[3] = np.nan
        output[4] = np.nan
    return output


for buoyid in buoyids.values():
    inppath = f"{DIRECTORY}/data/raw/buoy/{buoyid}_raw.txt"
    outpath = f"{DIRECTORY}/data/processed/buoy/{buoyid}_final.txt"
    df = pd.read_csv(inppath, sep=',')
    df = df[df['MM'] < 11]
    df = df[df['MM'] > 5]
    df = df.reset_index(drop=True)
    df_out = pd.DataFrame(columns=['YY', 'MM', 'DD', 'WDIRcos', 'WDIRsin', 'WSPD', 'ATMP'])
    for year in range (2012, 2024):
        for month in range (6, 11):
            for day in range (1, days[month - 1] + 1):
                output = to_day(df, year, month, day)
                df_out.loc[len(df_out.index)] = output

    df_out['YY'] = df_out['YY'].astype(int)
    df_out['MM'] = df_out['MM'].astype(int)
    df_out['DD'] = df_out['DD'].astype(int)
    df_out.to_csv(outpath, index=False)


