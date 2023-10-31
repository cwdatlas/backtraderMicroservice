import logging

import pytest

from Services.Trader import Trader
from models.BacktradeOptimize import BacktradeOptimize
from models.BacktradeTest import BacktradeTest

logger = logging.getLogger('unit_test_logger')


def test_backtrade_expected():
    data = {
        "start_date": {
            "year": "2007",
            "month": "1",
            "day": "1"
        },
        "end_date": {
            "year": "2022",
            "month": "1",
            "day": "1"
        },
        "stock_ticker": "UEC",
        "algorithm": "EMASMACROSS",
        "commission": ".01",
        "stake": "1",
        "sma": "30",
        "ema": "27"
    }
    backtest = BacktradeTest(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(backtest)
    assert results


def test_optimize_expected():
    data = {
        "start_date": {
            "year": "2007",
            "month": "1",
            "day": "1"
        },
        "end_date": {
            "year": "2022",
            "month": "1",
            "day": "1"
        },
        "stock_ticker": "UEC",
        "algorithm": "EMASMACROSS",
        "commission": ".01",
        "stake": "1",
        "start_sma": "10",
        "end_sma": "30",
        "start_ema": "10",
        "end_ema": "30"
    }
    test = BacktradeOptimize(**data)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results
