from pydantic.v1.dataclasses import dataclass


@dataclass
class TestReturn:
    sma: int
    ema: int
    ending_value: float
