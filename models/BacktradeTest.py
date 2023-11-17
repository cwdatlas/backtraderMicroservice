from pydantic.v1.dataclasses import dataclass

from models.BacktradeData import BacktradeData


@dataclass
class BacktradeTest(BacktradeData):
    sma: int
    ema: int

data = {
        "start_date": "2009-1-1",
        "end_date": "2009-1-2",
        "stock_ticker": "UEC",
        "algorithm": "SmaSmaCross",
        "commission": ".01",
        "stake": "1",
        "sma": "10",
        "ema": "10"
    }

test = BacktradeTest(**data)

