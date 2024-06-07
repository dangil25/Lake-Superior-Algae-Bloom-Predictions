import numpy as np
import pandas as pd
from config import DIRECTORY

buoy = "pngw3"

def round(x):
    x = str(x)
    ind = x.index('.')
    x = x[:ind] + x[ind:ind+3]
    return x

outlocation = DIRECTORY + f'/processor/processedData/alldata/{buoy}.txt'
emptyfillloc = DIRECTORY + f'/processor/data/buoy/{buoy}/emptyfill.xlsx'

df = pd.read_excel(emptyfillloc, sheet_name='emptyfill')

x = df['WTMP']

out = ""
for i in (x):
    try:
        out += round(i) +"\n"
    except:
        out += "    \n"
output = open(outlocation, "w")
output.write(out)
output.close()
