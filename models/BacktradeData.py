from dataclasses import dataclass
import datetime


@dataclass
class BacktradeData:
    start_date: datetime
    end_date: datetime
    stock_ticker: str
    algorithm: str
    commission: float
    stake: float
