import json
import logging

import werkzeug
from flask import Flask
from flask import request
from pydantic.v1.error_wrappers import ValidationError

from Services.Trader import Trader as Trader
from models.BacktradeOptimize import BacktradeOptimize
from models.BacktradeTest import BacktradeTest
from models.TestReturn import TestReturn

btrader = Flask(__name__)
logger = logging.getLogger('backtrade_logger')


@btrader.post('/optimize')
def optimize():
    logger.info(f"Request from {request.remote_addr}: {request.url}")
    # validating that data exists
    try:
        optimization = BacktradeOptimize(**request.get_json())
    except TypeError as e:
        return handle_bad_request(e)

    # validating that data is expected TODO test more complex validation
    if optimization.end_sma <= optimization.start_sma:
        return handle_bad_request(f"optimize: user gave improper start and end sma data: {str(optimization.end_sma)} {str(optimization.start_sma)}")
    if optimization.end_ema <= optimization.start_ema:
        return handle_bad_request(f"optimize: user gave improper start and end ema data: {str(optimization.end_ema)} {str(optimization.start_ema)}")
    trader = Trader()
    results = TestReturn(**{"ending_value": 1000, "ema": 20, "sma": 27})
    logger.debug(f"Optimize: returned successful Optimization: {str(results)}")
    return json.dumps(results.__dict__)


@btrader.post('/backtrade')
def backtrade():
    logger.info(f"Request from {request.remote_addr}: {request.url}")
    # validating that data exists
    try:
        test = BacktradeTest(**request.get_json())
    except TypeError as e:
        return handle_bad_request(e)

    # validating that data is expected TODO test more complex validation
    trader = Trader()
    results = TestReturn(**{"ending_value": 1000, "ema": 20, "sma": 27})
    logger.debug(f"backtrade: returned successful Optimization: {str(results)}")
    return json.dumps(results.__dict__)


@btrader.errorhandler(ValidationError)
def handle_bad_request(e):
    logger.exception(e)
    return json.dumps({"error": "Bad Request", "message": "inadequate or invalid data given. Make sure you have given " +
                                                          "all required valid variables"}), 400


@btrader.errorhandler(Exception)
def handle_unexpected_error(e):
    logger.exception(e)
    return json.dumps({"error": "Unexpected Error", "message": "An unexpected error occurred"}), 500
