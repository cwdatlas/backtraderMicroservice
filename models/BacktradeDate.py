from pydantic.v1.dataclasses import dataclass


@dataclass
class BacktradeDate:
    year: int
    month: int
    day: int