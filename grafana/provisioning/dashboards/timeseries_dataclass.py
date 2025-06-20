from dataclasses import dataclass
from typing import List, Dict, Optional, Any

@dataclass
class TimeSeriesTarget:
    expr: str
    legendFormat: str
    refId: str
    format: str = "time_series"

@dataclass
class TimeSeriesStacking:
    mode: str
    group: Optional[str] = None

@dataclass
class TimeSeriesConfig:
    title: str
    unit: str
    x_pos: int
    targets: List[TimeSeriesTarget]
    description: str = ""
    y_pos: int = 0
    lineWidth: int = 1
    fillOpacity: int = 30
    stacking: TimeSeriesStacking = TimeSeriesStacking(mode="none")
    extraJson: Dict[str, Any] = None

    def __post_init__(self):
        if self.extraJson is None:
            self.extraJson = {}
