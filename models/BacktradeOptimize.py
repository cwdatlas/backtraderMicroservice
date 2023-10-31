from models.BacktradeData import BacktradeData
from pydantic.v1.dataclasses import dataclass


@dataclass
class BacktradeOptimize(BacktradeData):
    start_sma: int
    end_sma: int
    start_ema: int
    end_ema: int
