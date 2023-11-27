from pydantic import model_validator

from Errors.MetricOutOfBoundsError import MetricOutOfBoundsError
from models.BacktradeData import BacktradeData


class BacktradeTest(BacktradeData):
    """
    BacktradeTest is used to store args for testing backtrades
    child of BacktradeData
    """
    sma: int
    ema: int

    @model_validator(mode='after')
    def backtrade_validation(self):
        """
        backtrade_validation validates BacktradeTest specific values

        :return:
            self
        """
        # set variables
        sma = self.sma
        ema = self.ema

        # validate values (must use basic if statements so errors can be understood easily)
        # sma and ema length validation
        if sma > 100:
            raise MetricOutOfBoundsError('SMA needs to be less than or equal to 100',
                                         "[sma]")  # "[sma]" stated at end to allow for easy error parsing in other midas applications
        if sma <= 1:
            raise MetricOutOfBoundsError('SMA  needs to more than or equal to 1', "[sma]")
        if ema > 100:
            raise MetricOutOfBoundsError('EMA needs to be less than or equal to 100', "[ema]")
        if ema <= 1:
            raise MetricOutOfBoundsError('EMA ema needs to more than or equal to 1', "[ema]")
        return self
