import backtrader as bt


# SMA Crossover Strategy
class SMACrossover(bt.Strategy):
    params = (
        ('short_period', 20),
        ('long_period', 50)
    )

    def __init__(self):
        self.sma1 = bt.indicators.MovingAverageSimple(period=self.params.short_period)
        self.sma2 = bt.indicators.MovingAverageSimple(period=self.params.long_period)

    def next(self):
        if self.sma1 > self.sma2:
            self.buy()
        elif self.sma1 < self.sma2:
            self.sell()
