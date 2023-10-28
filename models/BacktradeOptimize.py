from models.BacktradeData import BacktradeData
from dataclasses import dataclass


@dataclass
class BacktradeOptimize(BacktradeData):
    start_sma: int
    end_sma: int
    start_ema: int
    end_ema: int
