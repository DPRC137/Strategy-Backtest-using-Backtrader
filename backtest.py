import pandas as pd
import quantstats
import backtrader as bt
import datetime

from backtrader.feeds import PandasData

import backtrader.indicators as btind

# load dataframe

dataframe = pd.read_csv("BTC-USDd.csv")

dataframe['Date'] = pd.to_datetime(dataframe['Date'],format='%Y-%m-%d') 

class PandasData_Signal(PandasData):

    # Add a 'action' line to the inherited ones from the base class
    lines = ('signal',)

    # add the parameter to the parameters inherited from the base class
    params = (('signal', 8),)

data = PandasData_Signal(dataname=dataframe,

                    datetime=0,

                    open=1,

                    high=2,

                    low=3,

                    close=4,

                    volume=6,

                    signal=8,

                    #openinterest=-1,
                    fromdate = datetime.datetime(2015, 1,1)

                    )

class MLSignal(bt.SignalStrategy):

        def log(self, txt, dt=None):

            ''' Logging function for this strategy'''

            dt = dt or self.datas[0].datetime.date(0)

            print('%s, %s' % (dt.isoformat(), txt))


        def __init__(self):

            # Keep a reference to the "close" line in the data[0] dataseries

            self.dataclose = self.datas[0].close

            self.signal = self.datas[0].signal

            self.order = None

        
        def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                # Buy/Sell order submitted/accepted to/by broker - Nothing to do
                return

            # Check if an order has been completed
            # Attention: broker could reject order if not enough cash
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log(
                        'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                        (order.executed.price,
                        order.executed.value,
                        order.executed.comm))

                    self.buyprice = order.executed.price
                    self.buycomm = order.executed.comm
                else:  # Sell
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

            self.log(' Close, %.2f' % self.dataclose[0])

                    
            #Check if we are in the market 
            if not self.position :
                
                if self.signal[0] <= -0.15:

                    self.log('BUY CREATE, %.2f' % self.dataclose[0])

                    #Keep track of the created order to avoid a 2nd order
                    self.order = self.buy()
                    
            else:
                
                #Already in the market...we might sell
                if self.signal[0] >= 0.5:

                    self.log('SELL CREATE, %.2f' % self.dataclose[0]) 

                    self.order = self.sell()
                        

cerebro = bt.Cerebro()

   # Set our desired cash start

cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')

cerebro.broker.setcash(1000000.0)
cerebro.addsizer(bt.sizers.PercentSizer, percents= 95)

cerebro.adddata(data)

cerebro.addstrategy(MLSignal)
start = cerebro.broker.getvalue()
print('Initial Portfolio Value: %.2f' %cerebro.broker.getvalue())
#cerebro.run()

results = cerebro.run()
strat = results[0]

print('Final Portfolio Value: %.2f' %cerebro.broker.getvalue())
end = cerebro.broker.getvalue()
incPer = ((end - start) / start)*100
print('You made ' +str(incPer)+ ' percentage return from the initial investment')

portfolio_stats = strat.analyzers.getbyname('PyFolio')
returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
returns.index = returns.index.tz_convert(None)

quantstats.reports.html(returns, output='stats.html', title='BTC 30d Strategy')

cerebro.plot(iplot = False)
