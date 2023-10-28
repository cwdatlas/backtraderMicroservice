from Trader import Trader


class TraderCreator:
    def testAlgorithm(self):
        trader = Trader()
        return trader.execute_trade()
