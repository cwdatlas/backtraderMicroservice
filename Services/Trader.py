from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

import backtrader as bt

import Strategies
from Analyzers.EndingValueAnalyzer import EndingValueAnalyzer as EndValueA
from models.BacktradeOptimize import BacktradeOptimize
from models.BacktradeTest import BacktradeTest
from models.TestReturn import TestReturn


class Trader:
    def __init__(self):
        self.initial_capital = 1000

    def optimize_trade(self, params: BacktradeOptimize):
        if params is None:
            return None
        # Initialize Backtrader
        cerebro = bt.Cerebro()

        strategy_class = getattr(sys.modules[Strategies.__name__], params.algorithm)
        # Add a strategy
        cerebro.optstrategy(
            strategy_class,
            sma=range(params.start_sma, params.end_sma),
            ema=range(params.start_ema, params.end_ema))

        # Add data feed (replace with your data)
        modpath = os.path.dirname(os.path.abspath(sys.prefix))
        datapath = os.path.join(modpath, 'PriceHistory/UEC.csv')
        print('Absolute path found by os.path.abspath: %.2f' + datapath)
        data = bt.feeds.YahooFinanceCSVData(
            dataname=datapath,
            fromdata=datetime.datetime(params.start_date.year, params.start_date.month, params.start_date.day),
            todate=datetime.datetime(params.end_date.year, params.end_date.month, params.end_date.day),
            reverse=False)

        cerebro.adddata(data)
        cerebro.broker.setcash(self.initial_capital)
        cerebro.broker.setcommission(commission=params.commission)
        cerebro.addsizer(bt.sizers.FixedSize, stake=params.stake)
        # Add Analyzer to cerebro
        cerebro.addanalyzer(EndValueA, _name="End_Value_Analyzer")

        # Run Backtest
        results = cerebro.run()

        sma = 0
        ema = 0
        highest_g = 0
        for i in results:
            if i[0].analyzers[0].ending_value > highest_g:
                highest_g = i[0].analyzers[0].ending_value
                sma = i[0].params.sma
                ema = i[0].params.ema
        trade_results = TestReturn(**{"sma": sma, "ema": ema, "ending_value": round(highest_g, 2)})
        return trade_results

    def backtest(self, params: BacktradeTest):
        if params is None:
            return None
        # Initialize Backtrader
        cerebro = bt.Cerebro()

        strategy_class = getattr(sys.modules[Strategies.__name__], params.algorithm)
        # Add a strategy
        cerebro.addstrategy(
            strategy_class,
            sma=params.sma,
            ema=params.ema
        )

        # Add Analyzer to cerebro
        cerebro.addanalyzer(EndValueA, _name="End_Value_Analyzer")

        # Add data feed (replace with your data)
        modpath = os.path.dirname(os.path.abspath(sys.prefix))
        datapath = os.path.join(modpath, 'PriceHistory/UEC.csv')
        print('Absolute path found by os.path.abspath: %.2f' + datapath)
        data = bt.feeds.YahooFinanceCSVData(
            dataname=datapath,
            fromdata=datetime.datetime(params.start_date.year, params.start_date.month, params.start_date.day),
            todate=datetime.datetime(params.end_date.year, params.end_date.month, params.end_date.day),
            reverse=False)

        cerebro.adddata(data)
        cerebro.broker.setcash(self.initial_capital)
        cerebro.broker.setcommission(commission=params.commission)
        cerebro.addsizer(bt.sizers.FixedSize, stake=params.stake)

        # Run Backtest
        results = cerebro.run()
        trade_results = TestReturn(**{"sma": results[0].params.sma, "ema": results[0].params.ema,
                                      "ending_value": round(results[0].analyzers[0].ending_value, 2)})
        return trade_results
