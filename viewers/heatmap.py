import pandas as pd
from processor.config import DIRECTORY
import matplotlib
matplotlib.use('TkAgg')

buoy = 45028
location1 = DIRECTORY + f'/processor/data/buoy/{buoy}/daily.xlsx'

location = DIRECTORY + f'/processor/data/buoy/{buoy}/filleddaily.xlsx'
location2 = DIRECTORY + f'/processor/data/buoy/{buoy}/truncimputeddaily.xlsx'

df = pd.read_excel(location, sheet_name='filleddaily')
df1 = pd.read_excel(location2, sheet_name='truncimputeddaily')
df2 = pd.read_excel(location1, sheet_name = 'daily')

print (df.corr())
print(df1.corr())
print(df2.corr())
