from dataclasses import field

from pydantic.v1.dataclasses import dataclass


@dataclass
class TestReturn:# TODO rename objects to be the same on both java and python side
    """
    TestReturn returns backtrade test data to the user
    """
    sma: int = None
    ema: int = None
    ending_value: float = None
    error: str = None
    message: str = "Successful Operation"
    invalidators: str = None

