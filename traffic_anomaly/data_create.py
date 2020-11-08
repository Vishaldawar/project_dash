import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

list_banks = ['STATE BANK OF INDIA',
            'AXIS BANK',
            'HDFC BANK',
            'BANK OF BARODA',
            'KOTAK MAHINDRA BANK',
            'ICICI BANK']

short_names = ['sbi','axis','hdfc','bob','kotak','icici']

data = {}

for i in range(len(list_banks)):
    data[short_names[i]] = list_banks[i]

df = pd.DataFrame([list_banks,short_names]).T
df.columns = ['banks','short_names']

gran = '10min'
start = '2019-01-01'
end = '2019-06-01'
ts = pd.date_range(start=start, end=end, freq=gran)
mean = 1000
std = 150
np.random.seed(42)
ts_data = pd.DataFrame(ts)
ts_data.columns = ['_time']
for bank in short_names:
    val = mean+std*np.random.randn(ts.shape[0])
    ts_data[bank] = val
    ts_data[bank] = ts_data[bank].astype('int64')

ts_data = ts_data.reset_index(drop=True).set_index('_time')
ts_data.to_csv('./data_sources/traffic_data.csv')