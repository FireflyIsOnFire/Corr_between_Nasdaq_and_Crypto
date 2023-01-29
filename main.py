import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader.data as web
from datetime import date
import yfinance as yf
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
weights = [0.409,0.1745,0.0623,0.0123,0.192,0.082,0.012,0.0186,0.0186,0.0186]

df = pd.DataFrame()
price = pd.DataFrame()
for i in tickers:
    df[i] = yf.download(i, start, end)['Adj Close']

    if i == '^IXIC':
        nasdaq = df[i]
df.to_csv('database')
log_re = (np.log(df/df.shift(1))).iloc[1:,:]
data_op = log_re.iloc[:,:-1]
log_re.rename(columns = {'^IXIC':'NASDAQ'}, inplace = True) #inplace = True ensure to modigy the local data

#print(df.iloc[:,:10]*weights)
df['Portfolio'] = df.iloc[:,:10].apply(lambda x: x.sum(), axis=1)
#print(df.Portfolio)


# here assume assets are equally weighted
rolling_days7 = 7
rolling_days14 = 14
rolling_days30 = 30
ratio = 1/len(log_re.columns)
#weights = [0.3086,17.66]
log_re['portfolio'] = np.dot(log_re.iloc[:,:-1], weights)
log_re.to_csv('log_return')
nasdaq = (nasdaq.dropna(axis = 0, how = 'any'))[198:-1]

data_for_corr = log_re.dropna(axis = 0, how = 'any')
corr7 = ((data_for_corr['NASDAQ'].rolling(rolling_days7).corr(data_for_corr['portfolio'])).dropna(axis = 0, how = 'any'))[23:]
corr14 = (data_for_corr['NASDAQ'].rolling(rolling_days14).corr(data_for_corr['portfolio'])).dropna(axis = 0, how = 'any')[16:]
corr30 = (data_for_corr['NASDAQ'].rolling(rolling_days30).corr(data_for_corr['portfolio'])).dropna(axis = 0, how = 'any')

# plot the nasdaq trend and n-days rolling correlation:

cp = pd.DataFrame()
cp = pd.concat([df.Portfolio,nasdaq], axis =1)
cp = cp.dropna()
print(cp)

plt.style.use('bmh')
fig = plt.figure(figsize=(8,6))
ax1 = fig.add_subplot(211)
ax2 = ax1.twinx()
ax3 = fig.add_subplot(212)
ax1.set_ylabel('Crypto Asset/USD', fontsize = 13)
ax2.set_ylabel('Nasdaq/USD', fontsize = 13)
ax3.set_ylabel('Correlation', fontsize = 13)
ax1.plot(cp.Portfolio, label = 'Crypto Portfolio', color = 'orangered', linewidth = 1.)
ax2.plot(cp['^IXIC'], label = 'Nasdaq Composite', color = 'royalblue', linewidth = 1.)
ax1.legend()
ax2.legend(loc ='upper left')
ax3.plot(corr30, label = '30-days rolling correlation', color = 'navy', linewidth = 1)
ax3.legend()
#ax3.plot(corr14, label = '14-days rolling correlation', color = 'y', linewidth = 1 )
#ax3.plot(corr7, label = '7-days rolling correlation', color = 'c', linewidth = 1 )
plt.show()

'''plt.title('Correlation between Cryptos and Nasdaq')
ax1.set_ylabel('USD', fontsize = 15)
ax2.set_ylabel('Correlation',fontsize = 15)
ax1.plot(df.Portfolio, label = 'Crypto Asset', color = 'dodgerblue', linewidth = 1.5)
ax1.plot(nasdaq, label = 'Nasdaq Composites', color = 'k', linewidth = 1.5)
plt.legend()
#ax2.plot(corr7, label = '7-days rolling correlation', color = 'c', linewidth = 1 )
#ax2.plot(corr14, label = '14-days rolling correlation', color = 'y', linewidth = 1 )
ax2.plot(corr30, label = '30-days rolling correlation', color = 'navy', linewidth = 1 )
plt.legend()
plt.show()'''


