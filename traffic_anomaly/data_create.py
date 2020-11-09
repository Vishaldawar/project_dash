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
time_range_start = ['00:00:00','01:00:00','02:00:00','03:00:00','04:00:00','05:00:00','06:00:00',
                    '07:00:00','08:00:00','09:00:00','10:00:00','11:00:00','12:00:00','13:00:00',
                    '14:00:00','15:00:00','16:00:00','17:00:00','18:00:00','19:00:00','20:00:00',
                    '21:00:00','22:00:00','23:00:00']

time_range_end = ['01:00:00','02:00:00','03:00:00','04:00:00','05:00:00','06:00:00',
                    '07:00:00','08:00:00','09:00:00','10:00:00','11:00:00','12:00:00','13:00:00',
                    '14:00:00','15:00:00','16:00:00','17:00:00','18:00:00','19:00:00','20:00:00',
                    '21:00:00','22:00:00','23:00:00','23:59:59']
mean_time_wise = [100,120,130,150,160,180,200,
                    240,280,350,500,750,1000,750,
                    500,350,260,220,180,160,150,130,120,100]
std_time_wise = [8]*len(mean_time_wise)
std_time_pred = [12]*len(mean_time_wise)

def gen_values(row,time_range_start,time_range_end,mean_time_wise,std_time_wise):
    for i in range(len(time_range_start)):
        if row['hms'] >= time_range_start[i] and row['hms'] <= time_range_end[i]:
            return mean_time_wise[i] + std_time_wise[i]*np.random.randn()
        else:
            continue

np.random.seed(42)
ts_data = pd.DataFrame(ts)
ts_data.columns = ['_time']
ts_data['hms'] = ts_data['_time'].map(lambda x : x.strftime('%H:%M:%S'))
for bank in short_names:
    ts_data[bank] = ts_data.apply(gen_values,axis=1,args=(time_range_start,time_range_end,mean_time_wise,std_time_wise))
    ts_data[bank] = ts_data[bank].astype('int64')
    ts_data[bank+'_pred'] = ts_data.apply(gen_values,axis=1,args=(time_range_start,time_range_end,mean_time_wise,std_time_pred))
    

ts_data = ts_data.reset_index(drop=True).set_index('_time')
ts_data.drop('hms',axis=1,inplace=True)
#print(ts_data.head(20))
ts_data.to_csv('./data_sources/traffic_pred2.csv')