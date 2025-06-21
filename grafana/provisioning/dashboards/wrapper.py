from dataclasses import dataclass
from typing import Optional, Final

from grafanalib.core import Row, Dashboard, Target, TimeSeries, GridPos

from common import PROMETHEUS_DATASOURCE_NAME


class RefIdGenerator:
    STARTING_CHAR_INTEGER = ord("A")

    def __init__(self):
        self.offset = 0

    def next(self) -> str:
        result = chr(self.STARTING_CHAR_INTEGER + self.offset)
        self.offset += 1
        return result


@dataclass
class ExpressionAndLegendPair:
    expression: str
    legend: Optional[str] = None


class SceGrafanalibWrapper:
    MAX_WIDTH: Final[int] = 24

    def __init__(self, title, panel_width=12, panel_height=8):
        self.rows = []
        self.panels = []
        self.title = title
        self.current_x = 0
        self.current_y = 0
        self.panel_width = min(panel_width, self.MAX_WIDTH)
        self.panel_height = panel_height

    def AddPanel(self, title, queries: list[ExpressionAndLegendPair], unit='', dydt=False):
        targets = []
        iterator = RefIdGenerator()
        for query in queries:
            query_text = query.expression
            query_label = query.legend
            if dydt:
                total_query = f"sum({query_text})"
                rate_query = f"sum(rate({query_text}[1h]))"
                total_label = "total"
                rate_label = "dY/dt [hourly]"
                if query_label:
                    total_query += f' by ({query_label.strip("{}")})'
                    rate_query += f' by ({query_label.strip("{}")})'
                    total_label = f"{query_label} " + total_label
                    rate_label = f"{query_label} " + rate_label
                targets.append(
                    Target(
                        expr=total_query,
                        legendFormat=total_label,
                        refId=iterator.next(),
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                    )
                )
                targets.append(
                    Target(
                        expr=rate_query + " * 3600",
                        legendFormat=rate_label,
                        refId=iterator.next(),
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                    )
                )
            else:
                targets.append(
                    Target(
                        expr=query_text,
                        legendFormat=query_label,
                        refId=iterator.next(),
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                    )
                )
        self.panels.append(     
            TimeSeries(
                title=title,
                targets=targets,
                gridPos=GridPos(
                    h=self.panel_height,
                    w=self.panel_width,
                    x=self.current_x,
                    y=self.current_y,
                ),
                lineWidth=2,
                unit=unit
            )
        )
        self.current_x += self.panel_width
        if self.current_x > self.MAX_WIDTH / 2:
            self.current_y += self.panel_height
            self.current_x = 0

    def Render(self):
        return Dashboard(
            title=self.title, rows=self.rows, panels=self.panels, timezone='browser'
        ).auto_panel_ids()
