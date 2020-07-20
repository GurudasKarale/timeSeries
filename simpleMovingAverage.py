import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

#data preparation
data=pd.read_csv('.../TATA.csv')
dataname=pd.DataFrame(data)

dataname['Date']=pd.to_datetime(dataname['Date'])
dataname=dataname.set_index('Date')
print(dataname)

start_date=datetime(2017,10,1)
end_date=datetime(2018,10,8)

plt.plot(dataname[(start_date<=dataname.index) & (dataname.index<=end_date)]['Close'])
plt.show()


#apply sma
window_size=20
data_series = pd.Series(dataname[(start_date<=dataname.index) & (dataname.index<=end_date)]['Close'])
windows = data_series.rolling(window_size)
moving_averages = windows.mean()
#plt.plot(moving_averages)
#plt.show()

#plotting the data
fig, ax = plt.subplots(figsize=(16,9))
ax.plot(dataname[(start_date<=dataname.index) & (dataname.index<=end_date)]['Close'],label='Close')
ax.plot(moving_averages,label='Close_SMA')
plt.ylabel('Close')
plt.xlabel('Time')
plt.show()


