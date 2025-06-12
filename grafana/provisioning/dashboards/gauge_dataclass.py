from dataclasses import dataclass
from typing import List

@dataclass
class GaugeConfig:
    title: str
    description: str
    x_pos: int
    thresholds: List[int]
    expr: str
