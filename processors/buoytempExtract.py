import numpy as np
import pandas as pd
buoy = 45028

def round(x):
    x = str(x)
    ind = x.index('.')
    x = x[:ind] + x[ind:ind+3]
    return x

outlocation = f'C:/Users/danik2/Documents/School Files/Algae Research/python/processor/processedData/alldata/{buoy}.txt'
emptyfillloc = f'C:/Users/danik2/Documents/School Files/Algae Research/python/processor/data/buoy/{buoy}/emptyfill.xlsx'

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
