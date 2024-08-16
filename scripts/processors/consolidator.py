from config import *
import pandas as pd
import numpy as np

for group in range(1, 5):
    buoydf = pd.read_csv(f"{DIRECTORY}/data/processed/buoy/{buoyids[group]}_final.txt", sep = ',')
    sstdf = pd.read_csv(f"{DIRECTORY}/data/processed/sst/{sets[group][0]}_{sets[group][1]}.txt", sep = ",")
    riverdf = pd.read_csv(f"{DIRECTORY}/data/processed/river/discharge_{rivergroups[group]}_final.txt", sep = ",")

    #merges into a single df
    df = buoydf.merge(sstdf, on=['YY', 'MM', 'DD'], how='left')
    df = df.merge(riverdf, on=['YY', 'MM', 'DD'], how='left')

    #converts to datetime
    df["YY"] = df["YY"].astype(str)
    df["MM"] = df["MM"].astype(str)
    df["DD"] = df["DD"].astype(str)
    df.insert(0, "date", value = np.nan)
    df["date"] = df["YY"] + "-" + df["MM"] + "-" + df["DD"]
    df["date"] = pd.to_datetime(df["date"])
    df.drop(["YY", "MM", "DD"], axis=1, inplace=True)

    #adds bloom column
    df.insert(7, "bloom", value=0.0)

    #inserts bloom dates and adds
    for bloom in blooms[group]:
        index = df[df["date"] == pd.to_datetime(f"{bloom[0]}-{bloom[1]}-{bloom[2]}")].index.tolist()
        for offset in range(-5, 5):
            df.at[index[0] + offset, "bloom"] = round(1 - abs(offset)*0.2, 2)

    #sets index to be date
    df.set_index("date", inplace=True)

    #removes dates according to readme
    if (group == 1): pass
    if (group == 2): df = df[(df.index <= "2016-09-30") |
                             ((df.index >= "2017-06-01") & (df.index <= "2017-10-31")) |
                             (df.index >= "2020-06-01")]
    if (group == 3): df = df[(df.index <= "2018-10-31") |
                             (df.index >= "2020-06-01")]
    if (group == 4): df = df[((df.index >= "2013-06-01") & (df.index <= "2017-10-31")) |
                             (df.index >= "2019-06-01")]
    

    #saving before interpolation
    df.to_csv(f"{DIRECTORY}/data/final/group_{group}.txt")

    #time series interpolation

    df = df.interpolate(method='time')

    #saves df
    df.to_csv(f"{DIRECTORY}/data/final/group_{group}_interpolated.txt")



