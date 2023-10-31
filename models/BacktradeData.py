from pydantic.v1.dataclasses import dataclass
from models.BacktradeDate import BacktradeDate as date


@dataclass
class BacktradeData:
    start_date: date  # these are custom datatypes that match more closely to how the data will be used
    end_date: date
    stock_ticker: str
    algorithm: str
    commission: float
    stake: float
