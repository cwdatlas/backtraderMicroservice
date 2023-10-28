from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

import backtrader as bt

from Analyzers.EndingValueAnalyzer import EndingValueAnalyzer as EndValueA
from Strategies.TestStrategy import TestStrategy as TS
from models.TestReturn import TestReturn


class Trader:
    def __init__(self):
        self.initial_capital = 1000

    def optimize_trade(self, start_date, end_date, start_sma, end_sma, start_ema, end_ema, stock_ticker, stake, algorithm, commission):
        # Initialize Backtrader
        cerebro = bt.Cerebro()

        # Add a strategy
        cerebro.optstrategy(
            TS,
            maperiod=range(start_sma, end_sma))

        # Add Analyzer to cerebro
        cerebro.addanalyzer(EndValueA, _name="End_Value_Analyzer")

        # Add data feed (replace with your data)
        modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        datapath = os.path.join(modpath, 'PriceHistory/UEC.csv')
        print('Absolute path found by os.path.abspath: %.2f' + datapath)
        data = bt.feeds.YahooFinanceCSVData(
            dataname=datapath,
            fromdata=datetime.datetime(2020, 1, 1),
            todate=datetime.datetime(2023, 9, 13),
            reverse=False)

        cerebro.adddata(data)
        cerebro.broker.setcash(self.initial_capital)
        cerebro.broker.setcommission(commission=0.000)
        cerebro.addsizer(bt.sizers.FixedSize, stake=10)

        # Run Backtest
        results = cerebro.run()

        maperiod = 0
        highest_g = 0
        for i in results:
            if i[0].analyzers[0].ending_value > highest_g:
                highest_g = i[0].analyzers[0].ending_value
                maperiod = i[0].params.maperiod
        trade_results = TestReturn(maperiod, maperiod, round(highest_g, 2))
        return trade_results

    def backtest(self, start_date, end_date, sma, ema, stock_ticker, stake, algorithm, commission):

        # Initialize Backtrader
        cerebro = bt.Cerebro()

        # Add a strategy
        cerebro.addstrategy(
            TS,
            maperiod=sma)

        # Add Analyzer to cerebro
        cerebro.addanalyzer(EndValueA, _name="End_Value_Analyzer")

        # Add data feed (replace with your data)
        modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        datapath = os.path.join(modpath, 'PriceHistory/UEC.csv')
        print('Absolute path found by os.path.abspath: %.2f' + datapath)
        data = bt.feeds.YahooFinanceCSVData(
            dataname=datapath,
            fromdata=datetime.datetime(2020, 1, 1),
            todate=datetime.datetime(2023, 9, 13),
            reverse=False)

        cerebro.adddata(data)
        cerebro.broker.setcash(self.initial_capital)
        cerebro.broker.setcommission(commission=0.000)
        cerebro.addsizer(bt.sizers.FixedSize, stake=10)

        # Run Backtest
        results = cerebro.run()
        trade_results = TestReturn(results[0].params.maperiod, results[0].params.maperiod,
                                   round(results[0].analyzers[0].ending_value, 2))
        return trade_results
