import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader.data as web
from datetime import date
from OP_Portfolio import Op_Portfolio

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus']=False
pd.set_option('display.max_columns', None)

start = date(2020,1,1)
end = date.today()
interval = (end - start).days #days can't add ()
#print(interval)  #1048 days in total


#data collection:
tickers = ['BTC-USD','ETH-USD','USDT-USD','ADA-USD','XRP-USD','SOL-USD','DOGE-USD','DOT-USD','DAI-USD','MATIC-USD','^IXIC']

df = pd.DataFrame()
for i in tickers:
    df[i] = web.DataReader(i, 'yahoo', start, end)['Adj Close']

    if i == '^IXIC':
        nasdaq = df[i]
log_re = (np.log(df/df.shift(1))).iloc[1:,:]
data_op = log_re.iloc[:,:-1]
#print(len(data_op)) #10 assets, 1048 data
log_re.rename(columns = {'^IXIC':'NASDAQ'}, inplace = True) #inplace = True ensure to modigy the local data
log_re.to_csv('log_return')
#print(log_re, '\n'*2, nasdaq.head(10))

# here assume assets are equally weighted
rolling_days7 = 7
rolling_days14 = 14
rolling_days30 = 30
ratio = 1/len(log_re.columns)
weights = tuple(ratio for i in range(len(log_re.columns)-1))
log_re['portfolio'] = np.dot(log_re.iloc[:,:-1], weights)
nasdaq = (nasdaq.dropna(axis = 0, how = 'any'))[198:-1]
#diff = (date(2020,10,14) - date(2020,1,2)).days
#print(diff)
data_for_corr = log_re.dropna(axis = 0, how = 'any')
corr7 = ((data_for_corr['NASDAQ'].rolling(rolling_days7).corr(data_for_corr['portfolio'])).dropna(axis = 0, how = 'any'))[23:]
corr14 = (data_for_corr['NASDAQ'].rolling(rolling_days14).corr(data_for_corr['portfolio'])).dropna(axis = 0, how = 'any')[16:]
corr30 = (data_for_corr['NASDAQ'].rolling(rolling_days30).corr(data_for_corr['portfolio'])).dropna(axis = 0, how = 'any')


# plot the nasdaq trend and n-days rolling correlation:
plt.style.use('bmh')
fig = plt.figure(figsize=(8,6))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.set_ylabel('USD', fontsize = 15)
ax2.set_ylabel('Correlation',fontsize = 15)
ax1.plot(nasdaq, label = 'Nasdaq Composites', color = 'k', linewidth = 1.5)
ax2.plot(corr7, label = '7-days rolling correlation', color = 'c', linewidth = 1 )
ax2.plot(corr14, label = '14-days rolling correlation', color = 'y', linewidth = 1 )
ax2.plot(corr30, label = '30-days rolling correlation', color = 'b', linewidth = 1 )
plt.legend()
plt.show()












