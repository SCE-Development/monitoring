from dataclasses import dataclass
from typing import Optional, Final

from enum import Enum

from grafanalib.core import (
    Row,
    Dashboard,
    Target,
    TimeSeries,
    GridPos,
    GaugePanel,
    BarGauge,
    Stat,
    Template,
    Templating,
    REFRESH_ON_TIME_RANGE_CHANGE,
)

from common import PROMETHEUS_DATASOURCE_NAME


class PanelType(Enum):
    TIME_SERIES = TimeSeries
    GAUGE = GaugePanel
    BARGAUGE = BarGauge
    STAT = Stat


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
        self.templates = []

    def DefineRow(self, title):
        self.rows.append(Row(title=title, panels=[]))

    def DefineTemplating(
            self, 
            label, 
            query,
 
            ):
        self.templates.append(
            Template(
                name= label.lower().replace(" ", "_"),
                label=label,
                query=query,
                dataSource=PROMETHEUS_DATASOURCE_NAME,
                includeAll=True,
                multi=True,
                refresh=REFRESH_ON_TIME_RANGE_CHANGE,
            )
        )

    def AddPanel(
        self,
        title,
        queries: list[ExpressionAndLegendPair],
        unit="",
        dydt=False,
        panel_type_enum=PanelType.TIME_SERIES,
        lineWidth=None,
        fillOpacity=None,
        showPoints=None,
        stacking=None,
    ):
        targets = []
        iterator = RefIdGenerator()
        for query in queries:
            query_text = query.expression
            query_label = query.legend
            if not dydt:
                targets.append(
                    Target(
                        expr=query_text,
                        legendFormat=query_label,
                        refId=iterator.next(),
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                    )
                )
                continue
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

        panel = panel_type_enum.value(
            title=title,
            targets=targets,
            gridPos=GridPos(
                h=self.panel_height,
                w=self.panel_width,
                x=self.current_x,
                y=self.current_y,
            ),
        )
        if isinstance(panel, TimeSeries):
            if fillOpacity is not None:
                panel.fillOpacity = fillOpacity
            if showPoints is not None:
                panel.showPoints = showPoints
            if stacking is not None:
                panel.stacking = stacking
            if lineWidth is not None:
                panel.lineWidth = lineWidth

        # maybe only a few of the panel types are missing the unit field
        # unit_var = "unit" if hasattr(panel_type_enum.value, "unit") else "format"
        # setattr(panel, unit_var, unit)
        if hasattr(panel, "unit"):
            panel.unit = unit
        elif hasattr(panel, "format"):
            panel.format = unit
        row_or_panel = self.rows[-1].panels if self.rows else self.panels
        row_or_panel.append(panel)
        
        # Update position for next panel
        self.current_x += self.panel_width
        if self.current_x >= self.MAX_WIDTH:
            # Move to next row
            self.current_x = 0
            self.current_y += self.panel_height

    def Render(self):
        dashboard = Dashboard(
            title=self.title,
            rows=self.rows,
            panels=self.panels,
            timezone="browser",
            templating=Templating(list=self.templates),
        )
        
        return dashboard.auto_panel_ids()