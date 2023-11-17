import json
import logging

from flask import Flask
from flask import request
from pydantic.v1.error_wrappers import ValidationError

from Errors.BacktradeInputErrors import BacktradeInputErrors
from Services.Trader import Trader as Trader
from models.BacktradeOptimize import BacktradeOptimize
from models.BacktradeTest import BacktradeTest

btrader = Flask(__name__)
logger = logging.getLogger('backtrade_logger')


@btrader.post('/optimize')
def optimize():
    logger.info(f"Request from {request.remote_addr}: {request.url}")
    logger.debug(f"incoming body: {str(request.json)}")
    # validating that data exists
    try:
        optimization = BacktradeOptimize(**request.get_json())
    except TypeError as e:
        return handle_bad_request(e)

    # validating that data is expected TODO test more complex validation
    if optimization.end_sma <= optimization.start_sma:
        return handle_bad_request(
            f"optimize: user gave improper start and end sma data: {str(optimization.end_sma)} {str(optimization.start_sma)}")
    if optimization.end_ema <= optimization.start_ema:
        return handle_bad_request(
            f"optimize: user gave improper start and end ema data: {str(optimization.end_ema)} {str(optimization.start_ema)}")
    trader = Trader()
    results = trader.optimize_trade(optimization)
    logger.debug(f"Optimize: returned successful Optimization: {str(results)}")
    return json.dumps(results.__dict__)


@btrader.post('/backtrade')
def backtrade():
    logger.info(f"Request from {request.remote_addr}: {request.url}")
    logger.debug(f"incoming body: {str(request.json)}")
    # validating that data exists
    try:
        test = BacktradeTest(**request.get_json())
    except TypeError as e:
        return handle_bad_request(e)

    # validating that data is expected TODO test more complex validation
    trader = Trader()
    results = trader.backtest(test)
    logger.debug(f"backtrade: returned successful Optimization: {str(results)}")
    return json.dumps(results.__dict__)


@btrader.errorhandler(ValidationError)
def handle_bad_request(e):
    logger.exception("handle_bad_request: " + str(e.args))
    return json.dumps(
        {"error": "Bad Request", "message": e.args[0]}), 400


@btrader.errorhandler(BacktradeInputErrors)
def handle_backtrade_error(e):
    logger.exception("handle_backtrade_request" + str(e))
    return json.dumps(
        {"error": "Bad Data", "Message": str(e.args[0])}
    )


@btrader.errorhandler(ValueError)
def handle_value_error(e):
    logger.exception("handle_value_error: ")
    return json.dumps(
        {"error": "Bad Request", "message": "Make sure your dates and other params are accurate"}), 400


@btrader.errorhandler(AttributeError)
def handle_attribute_error(e):
    logger.exception("handle_attribute_error: " + str(e.args))
    return json.dumps(
        {"error": "Bad Request", "message": "Make sure your algorithm that you are using is correct"}), 400


@btrader.errorhandler(TypeError)
def handle_type_error(e):
    logger.exception("handle_type_error: " + str(e.args))
    return json.dumps(
        {"error": "Bad Request", "message": "Internal Error"}), 500


@btrader.errorhandler(Exception)
def handle_unexpected_exception(e):
    logger.exception("handle_unexpected_exception: s" + str(e.args))
    return json.dumps({"error": "Unexpected Error", "message": "An unexpected error occurred"}), 500


@btrader.after_request
def after_request(response):
    response.headers["Content-Type"] = "application/json"
    return response
