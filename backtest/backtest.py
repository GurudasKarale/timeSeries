import backtrader as bt
import backtrader.feeds as btfeeds
import os
import datetime


#custom indicators
class pch(bt.Indicator):
    lines = ('pch',)
    params = dict(period=5)


    def __init__(self):
        hi=self.datas[0]
        self.lines.pch = bt.ind.Highest(hi,period=self.params.period)

class pcl(bt.Indicator):
    lines = ('pcl',)
    params = dict(period=5)

    def __init__(self):
        lo=self.datas[0]
        self.lines.pcl = bt.ind.Lowest(lo,period=self.params.period)

"""
class hhpc(bt.Indicator):
    lines = ('hhpc',)
    params = dict(period=5)


    def __init__(self):
        lo=self.datas[0].low
        hi=self.datas[0].high
        for i in range(len(lo)):
            if lo[i] < bt.ind.Lowest(lo,period=self.params.period):
                self.lines.hhpc = bt.ind.Highest(hi,period=self.params.period)


class llpc(bt.Indicator):
    lines = ('llpc',)
    params = dict(period=5)


    def __init__(self):
       lo=self.datas[0].low
       hi=self.datas[0].high
       for i in range(len(hi)):
            if hi[i] > bt.ind.highest(hi,period=self.params.period):
                self.lines.llpc = bt.ind.Lowest(lo,period=self.params.period)

"""

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.myhigh = pch(self.datas[0].high)
        self.mylow = pcl(self.datas[0].low)
        #self.myhhpc = hhpc(self.datas[0])
        #self.myllpc = llpc(self.datas[0])

        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        bt.indicators.ExponentialMovingAverage(self.datas[0], period=5)      #indicator
        bt.indicators.ExponentialMovingAverage(self.datas[0].high, period=5)
        bt.indicators.ExponentialMovingAverage(self.datas[0].low, period=5)





    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:

            if self.dataclose[0] - self.dataclose[-1] > 3:

                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

        else:

            if self.dataclose[0] - self.dataclose[-1] < -3:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    datapath = os.path.abspath(os.getcwd() + '/HDFC_' + str(datetime.datetime.now().strftime("%Y_%m_%d")))

    # Create a Data Feed
    data = btfeeds.GenericCSVData(                                  #create generic data feed
        dataname=datapath,
        fromdate=datetime.datetime(2018,2,1),
        dtformat=('%Y-%m-%d %H:%M:%S'),
        timestamp=0,
        high=4,
        low=5,
        open=3,
        close=6,
        volume=7,
        timeframe= bt.TimeFrame.Minutes,
        #compression= 1
    )

    cerebro.adddata(data)

    cerebro.broker.setcash(1000.0)

    cerebro.addsizer(bt.sizers.FixedSize, stake=0.05)

    cerebro.broker.setcommission(commission=0.01)

    print('Starting Balance: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Balance: %.2f' % cerebro.broker.getvalue())

    cerebro.plot(style='candlestick')
