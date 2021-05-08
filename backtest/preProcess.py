from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import os
...
...
dataname='.../hdfc.csv'
datanamee=pd.read_csv(dataname)
datanamee=pd.DataFrame(datanamee)
#datanamee=datanamee.drop(['SYMBOL','INTERVAL'],axis=1)


from_date='01/09/2018'
now=datetime.now()
to_date=datetime.strftime(now,'%d/%m/%Y')


datanamee['DATE']=pd.to_datetime(datanamee['DATE'],unit='ns')
datanamee['DATE']=datanamee['DATE'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
datanamee.set_index('DATE',inplace=True)
datanamee.to_csv('HDFC_'+str(datetime.now().strftime('%Y_%m_%d')),date_format='%Y-%m-%d %H:%M:%S')
print(datanamee)

"""
datapath = os.path.abspath(os.getcwd() + 'C:/Users/Mohit K/PycharmProjects/hello/scratch/HDFC_2020_07_04' + str(datetime.now().strftime("%Y_%m_%d")))
data = btfeeds.GenericCSVData(
        dataname=datapath,
        fromdate=datetime(2018,9,1),
        dtformat=('%Y-%m-%d %H:%M:%S'),
        timestamp=0,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        timeframe= bt.TimeFrame.Minutes,
        compression= 1
    )

cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.run()
cerebro.plot()
"""
