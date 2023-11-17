import logging

import pytest
from pydantic import ValidationError

from Services.Trader import Trader
from models.BacktradeOptimize import BacktradeOptimize
from models.BacktradeTest import BacktradeTest

logger = logging.getLogger('unit_test_logger')


def test_optimize_expected():
    data = {
        "start_date": "2010-1-1",
        "end_date": "2010-2-1",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "10",
        "end_sma": "15",
        "start_ema": "10",
        "end_ema": "11"
    }
    test = BacktradeOptimize(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results.ending_value > 0


def test_optimize_expected_EE():
    data = {
        "start_date": "2010-1-1",
        "end_date": "2010-2-1",
        "stock_ticker": "UEC",
        "algorithm": "EmaEmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "10",
        "end_sma": "15",
        "start_ema": "10",
        "end_ema": "11"
    }
    test = BacktradeOptimize(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results.ending_value > 0


def test_optimize_expected_EE():
    data = {
        "start_date": "2010-1-1",
        "end_date": "2010-2-1",
        "stock_ticker": "UEC",
        "algorithm": "EmaEmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "10",
        "end_sma": "15",
        "start_ema": "10",
        "end_ema": "11"
    }
    test = BacktradeOptimize(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results.ending_value > 0


def test_optimize_expected_SS():
    data = {
        "start_date": "2010-1-1",
        "end_date": "2010-2-1",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "10",
        "end_sma": "15",
        "start_ema": "10",
        "end_ema": "11"
    }
    test = BacktradeOptimize(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results.ending_value > 0


def test_optimize_expected_low():
    data = {
        "start_date": "2010-1-1",
        "end_date": "2010-2-1",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": "0",
        "stake": "0",
        "start_sma": "1",
        "end_sma": "5",
        "start_ema": "1",
        "end_ema": "5"
    }
    test = BacktradeOptimize(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results.ending_value > 0


def test_optimize_expected_high():
    data = {
        "start_date": "2010-1-1",
        "end_date": "2010-2-1",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": "1",
        "stake": "100",
        "start_sma": "95",
        "end_sma": "100",
        "start_ema": "95",
        "end_ema": "100"
    }
    test = BacktradeOptimize(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results.ending_value > 0


def test_backtrade_expected():
    data = {
        "start_date": "2010-1-1",
        "end_date": "2010-2-1",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }
    test = BacktradeTest(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results.sma == 10
    assert results.ema == 10
    assert results.ending_value > 0


def test_backtrade_expected_EE():
    data = {
        "start_date": "2010-1-1",
        "end_date": "2010-2-1",
        "stock_ticker": "UEC",
        "algorithm": "EmaEmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }
    test = BacktradeTest(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results.sma == 10
    assert results.ema == 10
    assert results.ending_value > 0


def test_backtrade_expected_SS():
    data = {
        "start_date": "2010-1-1",
        "end_date": "2010-2-1",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }
    test = BacktradeTest(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results.sma == 10
    assert results.ema == 10
    assert results.ending_value > 0


def test_backtrade_expected_low():
    data = {
        "start_date": "2010-1-1",
        "end_date": "2010-2-1",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": "0",
        "stake": "0",
        "sma": "1",
        "ema": "1"
    }
    test = BacktradeTest(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results.sma == 1
    assert results.ema == 1
    assert results.ending_value == 1000


def test_backtrade_expected_high():
    data = {
        "start_date": "2010-1-1",
        "end_date": "2010-2-1",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": "1",
        "stake": "100",
        "sma": "100",
        "ema": "100"
    }
    test = BacktradeTest(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results.sma == 100
    assert results.ema == 100
    assert results.ending_value > 0


def test_backtrade_crappy_ss():
    data = {
        "start_date": "2009-1-1",
        "end_date": "2009-1-2",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except ValidationError as e:
        assert e
        test = e
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None
