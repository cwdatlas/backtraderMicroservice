import backtrader as bt


class EndingValueAnalyzer(bt.Analyzer):

    def __init__(self):
        self.ending_value = None

    def stop(self):
        self.ending_value = self.strategy.broker.getvalue()

    def get_analysis(self):
        return {"ending_value": self.ending_value}
