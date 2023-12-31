import os
import sys
from datetime import date
import logging
from pathlib import Path

from pydantic import model_validator, BaseModel

from Errors.AlgorithmNotFoundError import AlgorithmNotFoundError
from Errors.CommissionOutOfBoundsError import CommissionOutOfBoundsError
from Errors.DateInvalidError import DateInvalidError
from Errors.StakeOutOfBoundsError import StakeOutOfBoundsError
from Errors.TickerNotFoundError import TickerNotFoundError

logger = logging.getLogger('backtrade_logger')


class BacktradeData(BaseModel):
    """
    BacktradeData is the parent of the family of models used to create backtrades
    child of BaseModel from Pydantic, so it can act similar to a dataclass while still being a parent to other classes
    """
    start_date: date
    end_date: date
    stock_ticker: str
    algorithm: str  # must be one of the predefined algorithms
    commission: float
    stake: float  # must not be eaten

    @model_validator(mode='after')
    def general_validation(self):
        """
        Validator for all shared values between the backtrade family of models
        :return:
            self
        """
        # helpful objects
        # If DIR_HOME is specifically set as an environment variable.
        # This is used for running the app in a container
        modpath = os.environ.get("DIR_HOME")
        if modpath is None:
            modpath = os.path.dirname(os.path.abspath(sys.prefix))
        logger.debug(f"General path checking at '{modpath}'")

        # set variables
        start = self.start_date
        end = self.end_date
        commission = self.commission
        stake = self.stake
        stock_ticker = self.stock_ticker
        algorithm = self.algorithm

        # setting algorithm and stock_ticker paths
        alg_path = Path(os.path.join(modpath, f'Strategies/{algorithm}.py'))
        logger.debug(f"Algorithm path set to '{alg_path}'")
        ticker_path = Path(os.path.join(modpath, f'PriceHistory/{stock_ticker}.csv'))
        logger.debug(f"Ticker time series data path set to '{ticker_path}'")

        # validate values (must use basic if statements so errors can be understood easily)
        if start == end:
            raise DateInvalidError('dates are equal to each other', 'start_date')
        if start > end:
            raise DateInvalidError('Start date is later than end date', 'start_date')
        if commission > 1:
            raise CommissionOutOfBoundsError('Commission must be less or equal to 1', 'commission')
        if commission < 0:
            raise CommissionOutOfBoundsError('Commission needs to be more or equal to 0', 'commission')
        if stake > 100:
            raise StakeOutOfBoundsError('Stake needs to be less than or equal to 100', 'stake')
        if stake < 0:
            raise StakeOutOfBoundsError('Stake needs to be more than or equal to 0', 'stake')

        # algorithm validation
        if alg_path.exists() is False:
            raise AlgorithmNotFoundError("Algorithm could not be found", 'algorithm')

        # stock ticker validation
        if ticker_path.exists() is False:
            raise TickerNotFoundError("Input Ticker was not found in internal database", 'stock_ticker')
        return self
