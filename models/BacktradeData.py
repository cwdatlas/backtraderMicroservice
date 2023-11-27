from datetime import date

from pydantic import model_validator, BaseModel

from Errors.CommissionOutOfBoundsError import CommissionOutOfBoundsError
from Errors.DateInvalidError import DateInvalidError
from Errors.StakeOutOfBoundsError import StakeOutOfBoundsError


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
        # set variables
        start = self.start_date
        end = self.end_date
        commission = self.commission
        stake = self.stake
        #validate values (must use basic if statements so errors can be understood easily)
        if start == end:
            raise DateInvalidError('dates are equal to each other, start date must be before end date',
                                   '[start_date, end_date]')
        if start > end:
            raise DateInvalidError('Start date is later than end date, start date must be before end date',
                                   '[start_date, end_date]')
        if commission > 1:
            raise CommissionOutOfBoundsError('Commission must be less or equal to 1', '[commission]')
        if commission < 0:
            raise CommissionOutOfBoundsError('Commission needs to be more or equal to 0', '[commission]')
        if stake > 100:
            raise StakeOutOfBoundsError('Stake needs to be less than or equal to 100', '[stake]')
        if stake < 0:
            raise StakeOutOfBoundsError('Stake needs to be more than or equal to 0', '[stake]')
        return self




