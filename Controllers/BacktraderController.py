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
    """
    endpoint for all optimizations.

    Expected given format is json within the body of the request

    :return:
        TestReturn: the ending value, ema, and sma of the best trade based on ending value
    """
    logger.info(f"Request from {request.remote_addr}: {request.url}")
    logger.debug(f"incoming body: {str(request.json)}")
    # All validation happens here within the data class BacktradeOptimize
    try:
        optimization = BacktradeOptimize(**request.get_json())
    except TypeError as e:
        return handle_bad_request(e)

    trader = Trader()
    results = trader.optimize_trade(optimization)  # Find the best combination of imput args
    logger.debug(f"Optimize: returned successful Optimization: {str(results)}")
    return json.dumps(results.__dict__)


@btrader.post('/backtrade')
def backtrade():
    """
    Endpoint for all backtrades.

    Expected given format is json within the body of the request

    :return:
         TestReturn: the ending value, ema, and sma of the trade of the best test
    """
    logger.info(f"Request from {request.remote_addr}: {request.url}")
    logger.debug(f"incoming body: {str(request.json)}")
    # All validation happens here within the data class BacktradeOptimize
    try:
        test = BacktradeTest(**request.get_json())
    except TypeError as e:
        return handle_bad_request(e)

    trader = Trader()
    results = trader.backtest(test)  # check how well input args trade
    logger.debug(f"backtrade: returned successful Optimization: {str(results)}")
    return json.dumps(results.__dict__)


@btrader.errorhandler(ValidationError)
def handle_bad_request(e):
    """
    Catching global ValidationErrors from pycharm
    These are primarily raised in the input validation within our models

    :param e:
        The caught error
    :return:
        The error message, the error message
    """
    logger.exception("handle_bad_request: " + str(e.args))
    return json.dumps(
        {"error": "Bad Request", "message": e.args[0]}), 400  # considered user input error


@btrader.errorhandler(BacktradeInputErrors)
def handle_backtrade_error(e):
    """
    Catching global BacktradeInputErrors from midasbacktrader
    These are primarily raised in the input validation within our models

    :param e:
        The caught error
    :return:
        The error message, the error message
    """
    logger.exception("handle_backtrade_request" + str(e))
    return json.dumps(
        {"error": "Bad Data", "Message": str(e.args[0]), "invalidators": e.args[1]}), 400  # considered user input error


@btrader.errorhandler(ValueError)
def handle_value_error(e):
    """
    Catching global ValueErrors
    These are primarily raised in the input validation within our models

    :param e:
        The caught error
    :return:
        A generic error message (does not occur often)
    """
    logger.error(f"handle_value_error: '{str(e)}")
    return json.dumps(
        {"error": "Bad Request", "message": "Make sure all given parameters are accurate to the standard"}), 400
    # considered user input error


@btrader.errorhandler(AttributeError)
def handle_attribute_error(e):
    """
    Catching global AttributeErrors
    These are primarily raised when en error occurs in while backtrading or in prep for backtrading

    :param e:
        The caught error
    :return:
        A generic error message (does not occur often)
    """
    logger.exception("handle_attribute_error: " + str(e.args))
    return json.dumps(
        {"error": "Internal Error", "message": "Internal error"}), 500


@btrader.errorhandler(TypeError)
def handle_type_error(e):
    """
    Catching global TypeErrors
    These are primarily raised when en error occurs in while backtrading or in prep for backtrading
    If TypeErrors occur, then validation was not through enough, handle correction accordingly

    :param e:
        The caught error
    :return:
        A generic error message (does not occur often)
    """
    logger.exception("handle_type_error: " + str(e.args))
    return json.dumps(
        {"error": "Internal Error", "message": "Internal Error"}), 500


@btrader.errorhandler(Exception)
def handle_unexpected_exception(e):
    """
    Catching global Exceptions
    General exception, can happen anywhere. If another global error handler is not specific enough, then the error
    will be handled here. These exceptions are of great interest as they are totally unexpected behaviour,

    :param e:
        The caught error
    :return:
        A generic error message (does not occur often)
    """
    logger.exception("handle_unexpected_exception: s" + str(e.args))
    return json.dumps({"error": "Unexpected Error", "message": "An unexpected error occurred"}), 500


@btrader.after_request
def after_request(response):
    """
    After_request sets all headers to *application/json*
    This is important as other midas applications expect json to be returned

    :param response:
        any data from a return statement present in a http method
    :return:
        packet with json header to the user
    """
    response.headers["Content-Type"] = "application/json"
    return response
