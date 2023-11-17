from datetime import date

from pydantic import model_validator, BaseModel


class BacktradeData(BaseModel):
    start_date: date
    end_date: date
    stock_ticker: str
    algorithm: str
    commission: float
    stake: float

    @model_validator(mode='after')
    def general_validation(self):
        start = self.start_date
        end = self.end_date
        commission = self.commission
        stake = self.stake
        if start >= end:
            raise TypeError('dates are equal to each other, start date must be before end date')
        if commission > 1 or commission < 0:
            raise TypeError('Commission needs to be 0 <= commission <= 1')
        if stake > 100 or stake < 0:
            raise TypeError('Stake needs to be 0 <= stake <= 100')
        return self




