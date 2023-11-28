from dataclasses import field

from pydantic.v1.dataclasses import dataclass


@dataclass
class TestReturn:
    """
    TestReturn returns backtrade test data to the user
    """
    sma: int
    ema: int
    ending_value: float
    error: str = "None"
    message: str = "Successful Operation"
    invalidators: list = field(default_factory=list)

