from pydantic.dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int
