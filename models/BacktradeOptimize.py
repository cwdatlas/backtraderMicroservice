from pydantic import model_validator

from Errors.MetricOutOfBoundsError import MetricOutOfBoundsError
from models.BacktradeData import BacktradeData


class BacktradeOptimize(BacktradeData):
    """
    BacktradeOptimize is used to store args for optimization
    child of BacktradeData
    """
    start_sma: int
    end_sma: int
    start_ema: int
    end_ema: int

    @model_validator(mode='after')
    def optimize_validation(self):
        """
        optimize_validation validates BacktradeOptimize specific values

        :return:
            self
        """
        # set variables
        start_sma = self.start_sma
        end_sma = self.end_sma
        start_ema = self.start_ema
        end_ema = self.end_ema

        # validate values (must use basic if statements so errors can be understood easily)
        #start sma and ema validation
        if start_sma <= 0:
            raise MetricOutOfBoundsError('Starting SMA is 0 or lower', '[start_sma]')
        if start_ema <= 0:
            raise MetricOutOfBoundsError('Starting EMA is 0 or lower', '[start_ema]')
        if start_sma > 100:
            raise MetricOutOfBoundsError('Starting SMA must be less than 101', '[start_sma]')
        if start_ema > 100:
            raise MetricOutOfBoundsError('Starting EMA must be less than 101', '[start_ema]')

        #end sma and ema validation
        if end_sma <= 0:
            raise MetricOutOfBoundsError('Ending SMA is 0 or lower', '[end_sma]')
        if end_ema <= 0:
            raise MetricOutOfBoundsError('Ending EMA is 0 or lower', '[end_ema]')
        if end_sma > 100:
            raise MetricOutOfBoundsError('Ending SMA must be less than 100', '[end_sma]')
        if end_ema > 100:
            raise MetricOutOfBoundsError('Ending EMA must be less than 100', '[end_ema]')

        #validation making sure that starting is before ending
        if start_sma >= end_sma:
            raise MetricOutOfBoundsError('Starting SMA is larger or equal to ending SMA', '[start_sma, end_sma]')
        if start_ema >= end_ema:
            raise MetricOutOfBoundsError('Starting EMA is larger or equal to ending EMA', '[start_ema, end_ema]')
