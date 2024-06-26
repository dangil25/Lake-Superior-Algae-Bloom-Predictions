import torch
from torch import nn
from config import *
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import StandardScaler
import numpy as np
import torch

def df_to_X_y(df, window_size=14):
    df_as_np = (df.drop('bloom', axis = 1)).to_numpy()
    X = []
    y = df['bloom'][window_size:].values.tolist()
    for i in range(len(df_as_np)-window_size):
        row = np.array(df_as_np[i:i+window_size])
        # uncomment line below to flip rows and columns
        # row = row.transpose()
        X.append(row)
    return X, y


#preprocessing
df = []
X = []
y = []

for group in range (0, 4):
    df.append(pd.read_csv(f'{DIRECTORY}/data/final/group_{group + 1}_interpolated.txt', index_col=0))
    #changing index to datetime
    df[group].index = pd.to_datetime(df[group].index)

    #scaling
    standardscaler = StandardScaler()
    quantiletransformer = QuantileTransformer()

    standard = ['WSPD', 'ATMP', 'WTMP']
    quantile = ['DISC']
    df[group][standard] = standardscaler.fit_transform(df[group][standard])
    df[group][quantile] = quantiletransformer.fit_transform(df[group][quantile])

    #one-hot encoding groups
    df[group].insert(0, 'group1', float(0 == group))
    df[group].insert(1, 'group2', float(1 == group))
    df[group].insert(2, 'group3', float(2 == group))
    df[group].insert(3, 'group4', float(3 == group))

    #reshaping each feature into including 14 days before it: X is 14 arrays of 11 elements each.
    X_group, y_group = df_to_X_y(df[group], window_size=14)
    X.extend(X_group)
    y.extend(y_group)

print(X)
print(y)


















