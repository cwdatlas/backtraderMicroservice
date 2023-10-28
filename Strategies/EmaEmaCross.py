import backtrader as bt


# EMA Crossover Strategy
class EMACrossover(bt.Strategy):
    params = (
        ('short_period', 12),
        ('long_period', 26)
    )

    def __init__(self):
        self.ema1 = bt.indicators.ExponentialMovingAverage(period=self.params.short_period)
        self.ema2 = bt.indicators.ExponentialMovingAverage(period=self.params.long_period)

    def next(self):
        if self.ema1 > self.ema2:
            self.buy()
        elif self.ema1 < self.ema2:
            self.sell()