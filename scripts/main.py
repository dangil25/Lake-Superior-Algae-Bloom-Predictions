import torch
import torch.nn as nn
from config import *
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import torch

#TODO: Prevent contamination by only fitting scalers on training set

device = 'cuda:0' if torch.cuda.is_available() else "cpu"
print(device)
def df_to_X_y(df, window_size=14):
    #window size is the number of days into LSTM
    df_as_np = (df.drop('bloom', axis = 1)).to_numpy()
    X = []
    y = df['bloom'][window_size:].values.tolist()
    for i in range(len(df_as_np)-window_size):
        row = df_as_np[i:i+window_size]
        # uncomment line below to flip rows and columns
        # row = row.transpose()
        X.append(row.tolist())
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


X_tensor = torch.tensor(X, dtype=torch.float64)
print(X_tensor.shape)
print(X_tensor)
















