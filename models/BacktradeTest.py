from models.BacktradeData import BacktradeData
from pydantic.v1.dataclasses import dataclass


@dataclass
class BacktradeTest(BacktradeData):
    sma: int
    ema: int