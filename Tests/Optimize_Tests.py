import logging

from pydantic import ValidationError

from Errors.BacktradeInputErrors import BacktradeInputErrors
from Services.Trader import Trader
from models.BacktradeOptimize import BacktradeOptimize
from models.BacktradeTest import BacktradeTest

logger = logging.getLogger('unit_test_logger')


def test_optimize_expected():
    data = {
        "start_date": "2010-01-01",
        "end_date": "2010-02-01",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "10",
        "end_sma": "15",
        "start_ema": "10",
        "end_ema": "11"
    }

    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
        print(e)
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results.ending_value > 0


def test_optimize_expected_ee():
    data = {
        "start_date": "2010-01-01",
        "end_date": "2010-02-01",
        "stock_ticker": "UEC",
        "algorithm": "EmaEmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "10",
        "end_sma": "15",
        "start_ema": "10",
        "end_ema": "11"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
        assert e  # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results.ending_value > 0


def test_optimize_expected_ss():
    data = {
        "start_date": "2010-01-01",
        "end_date": "2010-02-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "10",
        "end_sma": "15",
        "start_ema": "10",
        "end_ema": "11"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
        assert e  # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results.ending_value > 0


def test_optimize_expected_low():
    data = {
        "start_date": "2010-01-01",
        "end_date": "2010-02-01",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": "0",
        "stake": "0",
        "start_sma": "1",
        "end_sma": "5",
        "start_ema": "1",
        "end_ema": "5"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
        assert e  # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results.ending_value > 0


def test_optimize_expected_high():
    data = {
        "start_date": "2010-01-01",
        "end_date": "2010-02-01",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": "1",
        "stake": "100",
        "start_sma": "95",
        "end_sma": "100",
        "start_ema": "95",
        "end_ema": "100"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
        assert e  # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.optimize_trade(test)
    assert results.ending_value > 0

def test_optimize_crappy_dates_equal():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2009-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "1",
        "end_sma": "2",
        "start_ema": "1",
        "end_ema": "2"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_otpimize_crappy_date_oposite():
    data = {
        "start_date": "2022-01-01",
        "end_date": "2009-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "1",
        "end_sma": "2",
        "start_ema": "1",
        "end_ema": "2"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crappy_sma_out_of_bounds_up():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "101",
        "end_sma": "102",
        "start_ema": "1",
        "end_ema": "2"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crappy_sma_out_of_bounds_down():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "-2",
        "end_sma": "-1",
        "start_ema": "1",
        "end_ema": "2"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crappy_ema_out_of_bounds_up():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "1",
        "end_sma": "2",
        "start_ema": "101",
        "end_ema": "102"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crappy_ema_out_of_bounds_down():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "start_sma": "1",
        "end_sma": "2",
        "start_ema": "-2",
        "end_ema": "-1"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crappy_stake_out_of_bounds_up():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "101",
        "start_sma": "1",
        "end_sma": "2",
        "start_ema": "1",
        "end_ema": "2"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crappy_stake_out_of_bounds_down():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "-1",
        "start_sma": "1",
        "end_sma": "2",
        "start_ema": "1",
        "end_ema": "2"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crappy_commission_out_of_bounds_up():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": "2",
        "stake": "1",
        "start_sma": "1",
        "end_sma": "2",
        "start_ema": "1",
        "end_ema": "2"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crappy_commission_out_of_bounds_down():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": "-1",
        "stake": "1",
        "start_sma": "1",
        "end_sma": "2",
        "start_ema": "1",
        "end_ema": "2"
    }
    try:
        test = BacktradeOptimize(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crazy_dates():
    data = {
        "start_date": "ajsfk;dhhhhhhhhhaskdjf",
        "end_date": "akskjndc;asojnrva;skjdn",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": "-1",
        "stake": "1",
        "start_sma": "1",
        "end_sma": "2",
        "start_ema": "1",
        "end_ema": "2"
    }
    try:
        test = BacktradeOptimize(**data)
    except ValidationError as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crazy_none():
    data = {
        "start_date": "None",
        "end_date": "None",
        "stock_ticker": "None",
        "algorithm": "None",
        "commission": "None",
        "stake": "None",
        "start_sma": "None",
        "end_sma": "None",
        "start_ema": "None",
        "end_ema": "None"
    }
    try:
        test = BacktradeOptimize(**data)
    except ValidationError as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crazy_blank():
    data = {
        "start_date": "",
        "end_date": "",
        "stock_ticker": "",
        "algorithm": "",
        "commission": "",
        "stake": "",
        "start_sma": "",
        "end_sma": "",
        "start_ema": "",
        "end_ema": ""
    }
    try:
        test = BacktradeOptimize(**data)
    except ValidationError as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


def test_optimize_crazy_incorrect_json():
    data = {
        "start_date": "",
        "end_date": "",
        "stock_ticker": "",
        "algorithm": "",
        "commission": "",
        "stake": "",
        "sma": "10",
        "ema": "10"
    }
    try:
        test = BacktradeOptimize(**data)
    except ValidationError as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None