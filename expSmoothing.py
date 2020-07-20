import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class smooth:

    def __init__(self,timeSeries,timeSeries1):
        self.timeSeries=timeSeries
        self.timeSeries1=timeSeries1

    def expSmooth(self):
        forecast=[np.mean(timeSeries)]
        forecast.append(timeSeries[0])
        alpha=0.3
        for i in range(1,len(timeSeries)-1):

            forecast.append((1-alpha)*forecast[-1]+alpha*timeSeries[i])


        return forecast

    def expTrend(self):
        alpha = 0.3
        beta = 0.3
        a=[timeSeries1[0]]
        b=[timeSeries1[1]-timeSeries1[0]]
        forecast=[np.mean(timeSeries1)]

        for i in range(1,len(timeSeries1)-1):
            forecast.append(a[i-1]+b[i-1])
            a.append(alpha*timeSeries1[i]+(1-alpha)*(a[i-1]+b[i-1]))
            b.append(beta*(a[i]-a[i-1])+(1-beta)*b[i-1])

        forecast.append(a[-1]+b[-1])
        a.append(forecast[-1])
        b.append(b[-1])
        return forecast,a,b

    def expDamped(self):
        alpha = 0.4
        beta = 0.4
        phi=0.8
        a=[timeSeries1[0]]
        b=[timeSeries1[1]-timeSeries1[0]]
        forecast=[np.mean(timeSeries1)]

        for i in range(1,len(timeSeries1)-1):
            forecast.append(a[i-1]+phi*b[i-1])
            a.append(alpha*timeSeries1[i]+(1-alpha)*(a[i-1]+phi*b[i-1]))
            b.append(beta*(a[i]-a[i-1])+(1-beta)*phi*b[i-1])

        forecast.append(a[-1]+b[-1])
        a.append(forecast[-1])
        b.append(b[-1])
        return forecast,a,b

    def mse(self,forecast):


        error=np.mean(np.abs(np.array(timeSeries)-np.array(forecast))**2)
        return error


    def dataPlot(self,forecast):

        plott={"original":timeSeries,"forecast":forecast}
        results = pd.DataFrame.from_dict(plott).round(0)
        results[["original","forecast"]].plot(title="Exponential Smoothing")
        return results

    def dataPlotTrend(self,forecast,level,trend):
        plott={"original":timeSeries1,"forecast":forecast,"level":level,"trend":trend}
        results = pd.DataFrame.from_dict(plott).round(0)
        results[["original","forecast"]].plot(title="Exponential Smoothing with trend")
        return results



timeSeries=[12,8,9,15,12,10,18,6,8,12,10,16,12,13,9]
timeSeries1=[50,68,85,111,133,143,161,180,193,185,193,215,228,224,226,249,228,231,214,
   185,204,193,187,167,148,121,95,88,87,119,125,134,131,126,127,138,135,
 129,166,175,166,157,158,187,193,161,169,167,149,138,132,136,98,124,122]

obj=smooth(timeSeries,timeSeries1)
smoo=obj.expSmooth()
pltt=obj.dataPlot(smoo)
print(obj.mse(smoo))
plt.plot(pltt)
plt.show()

f,l,t=obj.expTrend()
plott=obj.dataPlotTrend(f,l,t)
plt.plot(plott)
plt.show()

ff,ll,tt=obj.expDamped()
plot=obj.dataPlotTrend(ff,ll,tt)
plt.plot(plot)
plt.show()
