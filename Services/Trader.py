from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

import backtrader as bt

from Analyzers.EndingValueAnalyzer import EndingValueAnalyzer as EndValueA
from Strategies.TestStrategy import TestStrategy as TS
from models.TestReturn import TestReturn
from models.BacktradeOptimize import BacktradeOptimize
from models.BacktradeTest import BacktradeTest

class Trader:
    def __init__(self):
        self.initial_capital = 1000

    def optimize_trade(self, params: BacktradeOptimize):
        # Initialize Backtrader
        cerebro = bt.Cerebro()

        # Add a strategy
        cerebro.optstrategy(
            TS,
            maperiod=range(params.start_sma, params.end_sma))

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

        maperiod = 0
        highest_g = 0
        for i in results:
            if i[0].analyzers[0].ending_value > highest_g:
                highest_g = i[0].analyzers[0].ending_value
                maperiod = i[0].params.maperiod
        trade_results = TestReturn(**{"sma":maperiod, "ema":maperiod, "ending_value":round(highest_g, 2)})
        return trade_results

    def backtest(self, params: BacktradeTest):

        # Initialize Backtrader
        cerebro = bt.Cerebro()

        # Add a strategy
        cerebro.addstrategy(
            TS,
            maperiod=params.sma)

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
        trade_results = TestReturn(**{"sma" : results[0].params.maperiod, "ema": results[0].params.maperiod,
                                      "ending_value": round(results[0].analyzers[0].ending_value, 2)})
        return trade_results
