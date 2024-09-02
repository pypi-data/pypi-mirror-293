from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from tests.model.range import Range


@dataclass
class RangeWrapper:
    description: str
    interval: Range


@dataclass
class OptionalRangeWrapper:
    description: str
    interval: Optional[Range] = None


# noinspection PyArgumentList
@dataclass
class DefaultRangeWrapper:
    description: str
    interval: Range = Range(1, 10)
