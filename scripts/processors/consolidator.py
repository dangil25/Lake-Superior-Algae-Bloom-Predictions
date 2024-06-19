from config import *
import pandas as pd


for group in range(1, 5):
    buoydf = pd.read_csv(f"{DIRECTORY}/data/processed/buoy/{buoyids[group]}_final.txt", sep = ',')
    sstdf = pd.read_csv(f"{DIRECTORY}/data/processed/sst/{sets[group][0]}_{sets[group][1]}.txt", sep = ",")
    riverdf = pd.read_csv(f"{DIRECTORY}/data/processed/river/discharge_{rivergroups[group]}_final.txt", sep = ",")

    df = buoydf.merge(sstdf, on=['YY', 'MM', 'DD'], how='left')
    df = df.merge(riverdf, on=['YY', 'MM', 'DD'], how='left')

    #adds bloom column
    df.insert(8, "Bloom", False, True)

    #inserts bloom dates
    for bloom in blooms[group]:
        df.loc[(df.YY == bloom[0]) & (df.MM == bloom[1]) & (df.DD == bloom[2]), "Bloom"] = True

    df.to_csv(f"{DIRECTORY}/data/final/group_{group}.txt", index=False)



