from datetime import date

from pydantic import model_validator, BaseModel, ValidationError


class BacktradeData(BaseModel):
    start_date: date
    end_date: date
    stock_ticker: str
    algorithm: str
    commission: float
    stake: float

    @model_validator(mode='after')
    def date_relation_check(self):
        start = self.start_date
        end = self.end_date
        if start >= end:
            raise ValidationError('dates are equal to each other, start date must be before end date')
        return self
