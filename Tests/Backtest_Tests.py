import logging

from pydantic import ValidationError

from Errors.BacktradeInputErrors import BacktradeInputErrors
from Services.Trader import Trader
from models.BacktradeTest import BacktradeTest

logger = logging.getLogger('unit_test_logger')

"""
Any test with the word expected in the name contains data that should result in a successful operation
Any test with crappy in the name has invalid data in the json formatted string, and should result in an exception 
    when creating the backtrade type data type
Any test with crazy in the name has as wrong of data as possible given to the respective datatype, and should result in
    a None
"""


# Expected operation, containing data that should be valid
def test_backtrade_expected():
    data = {
        "start_date": "2010-01-01",
        "end_date": "2010-02-01",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except ValidationError as e:
        test = None
        assert e  # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results.sma == 10
    assert results.ema == 10
    assert results.ending_value > 0


# Expected operation specifically with the EmaEmaCross algorithm, containing data that should be valid
def test_backtrade_expected_ee():
    data = {
        "start_date": "2010-01-01",
        "end_date": "2010-02-01",
        "stock_ticker": "UEC",
        "algorithm": "EmaEmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except ValidationError as e:
        test = None
        assert e  # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results.sma == 10
    assert results.ema == 10
    assert results.ending_value > 0


# Expected operation specifically with the SmaSmaCross algorithm, containing data that should be valid
def test_backtrade_expected_ss():
    data = {
        "start_date": "2010-01-01",
        "end_date": "2010-02-01",
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
        test = None
        assert e  # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results.sma == 10
    assert results.ema == 10
    assert results.ending_value > 0


# Expected operation with the lowest expected inputs, containing data that should be valid
def test_backtrade_expected_low():
    data = {
        "start_date": "2010-01-01",
        "end_date": "2010-02-01",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": "0",
        "stake": "0",
        "sma": "1",
        "ema": "1"
    }
    try:
        test = BacktradeTest(**data)
    except ValidationError as e:
        test = None
        assert e  # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results.sma == 1
    assert results.ema == 1
    assert results.ending_value == 1000


# Expected operation with the highest expected inputs, containing data that should be valid
def test_backtrade_expected_high():
    data = {
        "start_date": "2010-01-01",
        "end_date": "2010-02-01",
        "stock_ticker": "UEC",
        "algorithm": "EmaSmaCross",
        "commission": "1",
        "stake": "100",
        "sma": "100",
        "ema": "100"
    }
    try:
        test = BacktradeTest(**data)
    except ValidationError as e:
        test = None
        assert e
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results.sma == 100
    assert results.ema == 100
    assert results.ending_value > 0


# Expected operation containing invalid same dates, containing data that should be not valid
def test_backtrade_crappy_dates_equal():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2009-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing invalid swapped dates, containing data that should be not valid
def test_backtrade_crappy_date_oposite():
    data = {
        "start_date": "2022-01-01",
        "end_date": "2009-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing out of bounds sma, over 100, containing data that should be not valid
def test_backtrade_crappy_sma_out_of_bounds_up():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "102",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing out of bounds sma, below 1, containing data that should be not valid
def test_backtrade_crappy_sma_out_of_bounds_down():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "-1",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing out of bounds ema, over 100, containing data that should be not valid
def test_backtrade_crappy_ema_out_of_bounds_up():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "10",
        "ema": "101"
    }
    try:
        test = BacktradeTest(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing out of bounds ema, below 1, containing data that should be not valid
def test_backtrade_crappy_ema_out_of_bounds_down():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "10",
        "ema": "-1"
    }
    try:
        test = BacktradeTest(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing out of bounds stake, over 100, containing data that should be not valid
def test_backtrade_crappy_stake_out_of_bounds_up():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "101",
        "sma": "10",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing out of bounds stake, below 0, containing data that should be not valid
def test_backtrade_crappy_stake_out_of_bounds_down():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "-1",
        "sma": "10",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing out of bounds commission, over 1, containing data that should be not valid
def test_backtrade_crappy_commission_out_of_bounds_up():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": "2",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing out of bounds commission, below 0, containing data that should be not valid
def test_backtrade_crappy_commission_out_of_bounds_down():
    data = {
        "start_date": "2009-01-01",
        "end_date": "2010-01-01",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": "-1",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except BacktradeInputErrors as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing invalid dates, containing data that should be not valid
def test_backtrade_crazy_dates():
    data = {
        "start_date": "ajsfk;dhhhhhhhhhaskdjf",
        "end_date": "akskjndc;asojnrva;skjdn",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": "-1",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }
    try:
        test = BacktradeTest(**data)
    except ValidationError as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing None for all values and incorrect json, containing data that should be not valid
def test_backtrade_crazy_none():
    data = {
        "start_date": "None",
        "end_date": "None",
        "stock_ticker": "None",
        "algorithm": "None",
        "commission": "None",
        "stake": "None",
        "sma": "None",
        "ema": "None"
    }
    try:
        test = BacktradeTest(**data)
    except ValidationError as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing empty strings for all values, containing data that should be not valid
def test_backtrade_crazy_blank():
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
        test = BacktradeTest(**data)
    except ValidationError as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None


# Expected operation containing empty strings for all values with incorrect json, containing data that should be not valid
def test_backtrade_crazy_incorrect_json():
    data = {
        "start_date": "",
        "end_date": "",
        "stock_ticker": "",
        "algorithm": "",
        "commission": "",
        "stake": "",
        "sma": "",
        "ema": ""
    }
    try:
        test = BacktradeTest(**data)
    except ValidationError as e:
        test = None
    assert test is None
    # after this point is the actual test, what is before is assumed to work
    trader = Trader()
    results = trader.backtest(test)
    assert results is None
