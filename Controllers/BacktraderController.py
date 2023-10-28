import json

from flask import Flask
from flask import request
from Services.Trader import Trader as Trader
from models.BacktradeOptimize import BacktradeOptimize

btrader = Flask(__name__)


@btrader.get('/test_connection')
def checkConnection():
    return "you can connect! good job"


@btrader.post('/optimize')
def optimize():
    #expected_p = {'endDate', 'startSma', 'endSma', 'startEma', 'endEma', 'stockticker', 'stake',
    #              'algorithm', 'commission'}
    #if not check_for_args(request.args, expected_p):
    #    return {'404 error': "lack of params, please provide" + str(expected_p)}
    print(str(request.get_json()))
    optimization = BacktradeOptimize(**json.dumps(request.get_json()))
    return optimization
    try:
        end_date = request.args.get(key='endDate')
        start_date = request.args.get(key='startDate', default='date')
        start_sma = int(float(request.args.get(key='startSma')))
        end_sma = int(float(request.args.get(key='endSma')))
        start_ema = int(float(request.args.get(key='startEma')))
        end_ema = int(float(request.args.get(key='endEma')))
        stock_ticker = request.args.get(key='stockticker')
        stake = float(request.args.get(key='stake'))
        algorithm = request.args.get(key='algorithm')
        commission = float(request.args.get(key='commission'))
    except Exception as e:
        print(optimization)
        return {'404 error': "unexpected params: " + str(e)}

    # TODO test more complex validation
    if (start_sma < end_sma) and (start_ema < end_ema):
        trader = Trader()
        results = trader.optimize_trade(start_date,end_date, start_sma, end_sma, start_ema, end_ema, stock_ticker,
                                        stake, algorithm, commission)
    else:
        results = '{error: "min must be less than max"}'

    if is_jsonable(results.to_dict()):
        return results.to_dict()  # TODO check if error returns 404 or other html status
    return "{error: cant send object}"


@btrader.post('/backtrade')
def backtrade():
    print(str(request.get_json()))
    expected_p = {'sma', 'ema', 'stockticker', 'stake', 'algorithm', 'commission'}
    if not check_for_args(request.args, expected_p):
        return {'404 error': "lack of params, please provide" + str(expected_p)}

    try:
        end_date = request.args.get(key='endDate', default='start')
        start_date = request.args.get(key='startDate', default='end')
        sma = int(float(request.args.get(key='sma')))
        ema = int(float(request.args.get(key='ema')))
        stock_ticker = request.args.get(key='stockticker')
        stake = float(request.args.get(key='stake'))
        algorithm = request.args.get(key='algorithm')
        commission = float(request.args.get(key='commission'))
    except Exception as e:
        print(e)
        return {'404 error': "unexpected params: " + str(e)}

    if sma and ema:
        trader = Trader()
        results = trader.backtest(start_date, end_date, sma, ema, stock_ticker, stake, algorithm, commission)
    else:
        results = '{error: "maperiod must not be nil"}'

    if is_jsonable(results.to_dict()):
        return results.to_dict()
    return "{error: cant send object}"  # TODO check if error returns 404 or other html status


def check_for_args(args, expected_p):
    valid = True
    print("all Params are" + str(args.to_dict()))
    for i in expected_p:
        param = args.get(key=i)
        if param is None:
            valid = False
            print("Param missing: " + i)
    return valid


def is_jsonable(obj):
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        print("Error parsing object: " + str(obj))
        return False
