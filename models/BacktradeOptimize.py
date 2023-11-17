from pydantic.dataclasses import dataclass

from models.BacktradeData import BacktradeData


@dataclass
class BacktradeOptimize(BacktradeData):
    start_sma: int
    end_sma: int
    start_ema: int
    end_ema: int

