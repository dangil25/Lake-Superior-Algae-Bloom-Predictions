import torch
from torch import nn
from config import *
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import StandardScaler
import numpy as np
import torch

def df_to_X_y(df, window_size=5):
  df_as_np = df.to_numpy()
  X = []
  y = []
  for i in range(len(df_as_np)-window_size):
    row = [[a] for a in df_as_np[i:i+window_size]]
    X.append(row)
    label = df_as_np[i+window_size]
    y.append(label)
  return np.array(X), np.array(y)


#preprocessing
df = []

#global df combining all four locations, with one-hot encoding for location
global_df = pd.DataFrame(columns=['group1', 'group2', 'group3', 'group4', 'WDIRcos', 'WDIRsin', 'WSPD', 'ATMP', 'WTMP', 'DISC', 'bloom'])

for group in range (0, 4):
    df.append(pd.read_csv(f'{DIRECTORY}/data/final/group_{group + 1}.txt', index_col=0))
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
    df[group].insert(0, 'group1', int(0 == group))
    df[group].insert(1, 'group2', int(1 == group))
    df[group].insert(2, 'group3', int(2 == group))
    df[group].insert(3, 'group4', int(3 == group))

    #reshaping each feature into including 14 days before it,
















