from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import logging
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
from pathlib import Path

import backtrader as bt

import Strategies
from Analyzers.EndingValueAnalyzer import EndingValueAnalyzer as EndValueA
from Errors.AlgorithmNotFoundError import AlgorithmNotFoundError
from Errors.TickerNotFoundError import TickerNotFoundError
from models.BacktradeOptimize import BacktradeOptimize
from models.BacktradeTest import BacktradeTest
from models.TestReturn import TestReturn

logger = logging.getLogger('backtrade_logger')


class Trader:
    """
    Trader contains the functions that set up trades like optimization and backtrade
    """

    def __init__(self):
        self.initial_capital = 1000  # Default initial capitol, makes growth easy to see
        # TODO impliment percentage return

    def optimize_trade(self, params: BacktradeOptimize) -> TestReturn:
        """
        optimize_trade takes params and finds the optimal trading strategy with past stock data based on param guidelines
        :param
            params: BacktradeOptimize
        :return:
            TestReturn: generic return format for test results
        """
        # allows for flexibility when testing
        if params is None:
            return None

        # Initialize Backtrader
        cerebro = bt.Cerebro()

        # check if strategy is found
        strategy_class = getattr(sys.modules[Strategies.__name__], params.algorithm)
        cerebro.optstrategy(
            strategy_class,
            sma=range(params.start_sma, params.end_sma),
            ema=range(params.start_ema, params.end_ema))

        # Add data feed
        modpath = os.path.dirname(os.path.abspath(sys.prefix))
        datapath = os.path.join(modpath, f'PriceHistory/{params.stock_ticker}.csv')
        file_path = Path(datapath)

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
        # initialising TestReturn
        trade_results = TestReturn(**{"sma": sma,
                                      "ema": ema,
                                      "ending_value": round(highest_g, 2)})
        return trade_results

    def backtest(self, params: BacktradeTest) -> TestReturn:
        """
        backtest takes params and finds trades with the set guidelines
        :param
            params: BacktradeTest
        :return:
            TestReturn: generic return format for test results
        """
        # allows for flexibility when testing
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

        # Add data feed
        modpath = os.path.dirname(os.path.abspath(sys.prefix))

        datapath = os.path.join(modpath, f'PriceHistory/{params.stock_ticker}.csv')
        file_path = Path(datapath)

        data = bt.feeds.YahooFinanceCSVData(
            dataname=datapath,
            fromdata=datetime.datetime(params.start_date.year, params.start_date.month, params.start_date.day),
            todate=datetime.datetime(params.end_date.year, params.end_date.month, params.end_date.day),
            reverse=False)
        logger.info('Absolute path found by os.path.abspath: %.2f' + datapath)

        cerebro.adddata(data)
        cerebro.broker.setcash(self.initial_capital)
        cerebro.broker.setcommission(commission=params.commission)
        cerebro.addsizer(bt.sizers.FixedSize, stake=params.stake)

        # Run Backtest
        results = cerebro.run()
        # initialising TestReturn
        trade_results = TestReturn(**{"sma": results[0].params.sma,
                                      "ema": results[0].params.ema,
                                      "ending_value": round(results[0].analyzers[0].ending_value, 2)})
        return trade_results
