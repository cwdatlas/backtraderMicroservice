from pydantic import model_validator
from pydantic.v1.dataclasses import dataclass

from Errors.MetricOutOfVoundsError import MetricOutOfBoundsError
from models.BacktradeData import BacktradeData


class BacktradeTest(BacktradeData):
    sma: int
    ema: int

    @model_validator(mode='after')
    def optimize_validation(self):
        sma = self.sma
        ema = self.ema
        if sma > 100 or sma <= 0:
            raise MetricOutOfBoundsError('SMA is out of bounds, needs to be inbetween 101 and 0')
        if ema > 100 or ema <= 0:
            raise MetricOutOfBoundsError('EMA is out of bounds, needs to be inbetween 101 and 0')
        return self
