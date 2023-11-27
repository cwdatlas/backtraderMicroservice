import backtrader as bt


class EndingValueAnalyzer(bt.Analyzer):
    """
    EndingValueAnalyzer is used to gather the ending value from a cerebro trade instance
    Pass EndingValueAnalyzer into cerebro.optstragegy or .addstrategy
    """

    def __init__(self):
        self.ending_value = None

    def stop(self):
        """
        gets stores the value of the trade so it can be accessed after all trades are complete
        """
        self.ending_value = self.strategy.broker.getvalue()

    def get_analysis(self):
        """
        :returns:
            int: ending value of the last trade
        """
        return {"ending_value": self.ending_value}
