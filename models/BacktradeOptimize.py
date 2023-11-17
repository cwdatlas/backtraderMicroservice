from pydantic import model_validator

from Errors.MetricOutOfVoundsError import MetricOutOfBoundsError
from models.BacktradeData import BacktradeData


class BacktradeOptimize(BacktradeData):
    start_sma: int
    end_sma: int
    start_ema: int
    end_ema: int

    @model_validator(mode='after')
    def backtrade_validation(self):
        start_sma = self.start_sma
        end_sma = self.end_sma
        start_ema = self.start_ema
        end_ema = self.end_ema

        if start_sma <= 0:
            raise MetricOutOfBoundsError('Starting SMA is 0 or lower, must be more than 0 and less than 101')
        if start_ema <= 0:
            raise MetricOutOfBoundsError('Starting EMA is 0 or lower, must be more than 0 and less than 101')
        if start_sma > 100:
            raise MetricOutOfBoundsError('Starting SMA is 101 or higher, must be more than 0 and less than 101')
        if start_ema > 100:
            raise MetricOutOfBoundsError('Starting EMA is 101 or higher, must be more than 0 and less than 101')

        if end_sma <= 0:
            raise MetricOutOfBoundsError('Ending SMA is 0 or lower, must be more than 0 and less than 101')
        if end_ema <= 0:
            raise MetricOutOfBoundsError('Ending EMA is 0 or lower, must be more than 0 and less than 101')
        if end_sma > 100:
            raise MetricOutOfBoundsError('Ending SMA is 101 or higher, must be more than 0 and less than 101')
        if end_ema > 100:
            raise MetricOutOfBoundsError('Ending EMA is 101 or higher, must be more than 0 and less than 101')

        if start_sma >= end_sma:
            raise MetricOutOfBoundsError('Starting SMA is larger or equal to ending SMA')
        if start_ema >= end_ema:
            raise MetricOutOfBoundsError('Starting EMA is larger or equal to ending EMA')
