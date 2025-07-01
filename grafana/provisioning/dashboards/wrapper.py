from dataclasses import dataclass, field
from typing import List, Optional, Union
from grafanalib.core import Dashboard, Panel, Row, GridPos, TimeSeries, Target
import string

@dataclass
class QueryDef:
    query: str
    title: Optional[str] = None

@dataclass
class DashboardWrapper:
    title: str
    description: str
    timezone: str = 'browser'
    tags: List[str] = field(default_factory=list)

    # Internal list to hold Panel objects.
    _rows: List[Row] = field(default_factory=list, init=False, repr=False)
    _current_row: int = field(default=0, init=False, repr=False)
    _panel_x: int = field(default=0, init=False, repr=False)
    _panel_y: int = field(default=0, init=False, repr=False)
    _panel_height: int = field(default=8, init=False, repr=False)
    _panel_width: int = field(default=12, init=False, repr=False)

    def define_row(self, title: str):
        self._rows.append(Row(title=title))
        self._panel_x = 0
        self._panel_y = self._current_row * self._panel_height
        self._current_row += 1
        return self

    def add_time_series_panel(self, title: str, queries: List[QueryDef], unit=None, lineWidth=2, datasource='Prometheus'):
        gridPos = GridPos(h=self._panel_height, w=self._panel_width, x=self._panel_x, y=self._panel_y)
        targets = []
        for i, q in enumerate(queries):
            if isinstance(q, QueryDef):
                expr = q.query
                legendFormat = q.title
            else:
                raise ValueError("Each query must be a QueryDef or a (query, title) tuple")
            targets.append(Target(
                datasource=datasource,
                expr=expr,
                legendFormat=legendFormat,
                refId=string.ascii_uppercase[i]
            ))
        panel = TimeSeries(
            title=title,
            unit=unit,
            gridPos=gridPos,
            lineWidth=lineWidth,
            targets=targets,
        )
        self.add_panel(panel)
        self._panel_x += self._panel_width
        return self

    def add_panel(self, panel: Panel):
        if len(self._rows) < 1:
            raise ValueError("No row defined. Call define_row() first.")
        self._rows[-1].panels.append(panel)
        return self

    def render(self) -> Dashboard:
        return Dashboard(
            title=self.title,
            description=self.description,
            timezone=self.timezone,
            tags=self.tags,
            rows=self._rows,
        )
