import numpy as np
import pandas as pd
import requests
from processor.config import *


# buoy to process

# splits array of strings into array of lists of floats (strips last because it is blank)
def splitter(inp):
    inp = inp.split('\n')
    for line in range(len(inp)):
        inp[line] = inp[line].split()
    out = np.array(inp[:-1], dtype=float)
    return out


# downloads all the data returns heading w column headings, and output with outputs
def download(buoy):
    out = ""
    head = ""
    for year in range(2012, 2024):
        url = f'https://www.ndbc.noaa.gov/view_text_file.php?filename={buoy}h{year}.txt.gz&dir=data/historical/stdmet/'
        print(url)
        req = requests.get(url, allow_redirects=True)
        out += req.content.decode('utf-8')[178:]
        head = req.content.decode('utf-8')[1:89]
    return head, out


for buoyid in buoyids:
    print(buoyid)
    heading, data = download(buoyid)
    print(heading)
    df = pd.DataFrame(splitter(data), columns=heading.split())
    df = df.drop(columns=['hh', 'mm', 'GST', 'WVHT', 'DPD', 'APD', 'MWD', 'PRES', 'WTMP', 'DEWP', 'VIS', 'TIDE'])
    df['ATMP'].replace([999.0, 99.0], np.nan, inplace=True)
    df.to_string(f"{DIRECTORY}/processor/data/buoy/{buoyid}_raw.txt", index=False)
