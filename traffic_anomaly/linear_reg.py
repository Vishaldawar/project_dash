import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
import os

traffic = pd.read_csv(os.getcwd() + '/data_sources/traffic_data.csv',index_col=0)

banks = traffic.columns.tolist()

data = traffic.copy()

data['year'] = data.index.map(lambda x : int(x[:4]))
data['year'] = data['year'] - data['year'].min() + 1
data['month'] = data.index.map(lambda x : int(x[5:7]))
data['day'] = data.index.map(lambda x : int(x[8:10]))
data['hour'] = data.index.map(lambda x : int(x[11:13]))
data['minute'] = data.index.map(lambda x : int(x[14:16]))
data['quarter'] = data['month'].map(lambda x : int(x/4)+1)


columns = ['year','month','day','hour','minute','quarter']
train_X = data[columns]
for bank in banks:
    train_y = data[bank]
    X = train_X.copy()
    #X = sm.add_constant(X, has_constant='add')
    #model = sm.OLS(train_y.astype(float), X.astype(float)).fit()
    model = LinearRegression().fit(X,train_y)
    pred = model.predict(X)
    print("For bank : ",bank," Rsquared value is : ",round(r2_score(train_y,pred),3))
    data[bank+'_pred'] = pred


data.to_csv('./data_sources/traffic_pred.csv')