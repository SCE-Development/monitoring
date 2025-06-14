from grafanalib.core import (
    Row, Panel, Dashboard, Target, TimeSeries, GridPos
)

class Iterator:
    def __init__(self, start='A', end='Z', range=26):
        self.start = start
        self.end = end
        self.range = range
        self.count = 0

    def next(self):
        self.char = chr(ord(self.start) + self.count % self.range)
        self.count += 1
        return self.char
    
from dataclasses import dataclass
from typing import Optional, Final

@dataclass
class ExpressionAndLegend:
    expression: str
    legend: Optional[str] = None

from common import PROMETHEUS_DATASOURCE_NAME

class Wrapper:
    MAX_WIDTH: Final[int] = 24

    def __init__(self, title, panel_width=12, panel_height=8):
        self.rows = []
        self.panels = []
        self.title = title
        self.current_x = 0
        self.current_y = 0
        self.panel_width = min(panel_width, self.MAX_WIDTH)
        self.panel_height = panel_height

    def DefineRow(self, title):
        self.rows.append(Row(title=title, panels=[]))

    def AddPanelToRow(self, title, queries: list[ExpressionAndLegend]):
        if (len(self.rows) == 0):
            return ValueError
        targets = []
        iterator = Iterator()
        for query in queries:
            query_text = query.expression
            query_label = query.legend
            refId = iterator.next()
            targets.append(Target(expr=query_text, legendFormat=query_label, refId=refId, datasource=PROMETHEUS_DATASOURCE_NAME))
        self.rows[-1].panels.append(TimeSeries(title=title, targets=targets))

    def AddPanel(self, title, queries: list[ExpressionAndLegend]):
        targets = []
        iterator = Iterator()
        for query in queries:
            query_text = query.expression
            query_label = query.legend
            refId = iterator.next()
            targets.append(Target(expr=query_text, legendFormat=query_label, refId=refId, datasource=PROMETHEUS_DATASOURCE_NAME))
        self.panels.append(TimeSeries(title=title, targets=targets, gridPos=GridPos(h=self.panel_height, w=self.panel_width, x=self.current_x, y=self.current_y)))
        self.current_x += self.panel_width
        if self.current_x >= self.MAX_WIDTH/2:
            self.current_y += self.panel_height
            self.current_x = 0

    def Render(self):
        return Dashboard(
            title=self.title,
            rows=self.rows,
            panels=self.panels 
        ).auto_panel_ids()