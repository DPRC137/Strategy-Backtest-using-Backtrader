# Strategy Backtest using Backtrader
Backtesting a 30d-Returns based strategy with Backtrader and making a report with Quantstats. Done on BTC-USDT historical data.


![result](https://user-images.githubusercontent.com/50619554/173841041-76f4108d-9b90-40ef-b79f-21d6d3ec160e.png)


## 30d Returns
30-day Returns are calculated on the price historical. This is already saved adn has been changed to percentages under the label "signal".

## Strategy
Backtrader will execute BUY when the pct change in signal is -15%.

The Position is held until the pct change in signal is +50%, then a SELL order is triggered and the position will be closed.

## Report
A detailed report is generated at the end of the execution using Quantstats and saved inside the dir as "stats.html".![Screenshot (164)](https://user-images.githubusercontent.com/50619554/173845261-b277f0d6-6862-4036-a262-886bb7e67e6a.jpg)
