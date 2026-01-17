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

    def __init__(self, title, description="", panel_width=12, panel_height=8):
        self.rows = []
        self.panels = []
        self.title = title
        self.description = description
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

    def CreatePanel(self,
        title,
        queries: list[ExpressionAndLegendPair],
        unit="",
        dydt=False,
        panel_type_enum=PanelType.TIME_SERIES,
        lineWidth=None,
        fillOpacity=None,
        showPoints=None,
        stacking=None,
        extraJson=None):

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
            extraJson=extraJson,
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
        return panel

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
        extraJson=None,
    ):
        '''
        Add panel under a new defined row
        
        :param title: panel title
        :param queries: Description
        :type queries: list[ExpressionAndLegendPair] 
        :param unit: Y-axis unit/format 'percent' , 'bytes/sec', 'short'
        :param dydt: if true aluto-generates two targets per query
        :param panel_type_enum: panel visualization PanelType.TIME_SERIES , PanelType.GAUGE , PanelType.BARGAUGE , PanelType.STAT
        :param lineWidth: line thickness 1-10
        :param fillOpacity: area fill transparency 0.0-1.0
        :param showPoints: point visibility "never" , "auto" , "always"
        :param stacking: stacking mode "off" , "normal" , "100%"
        :param extraJson: dict of raw JSON for panel constructor
        '''
    
        panel = self.CreatePanel(
            title,
            queries,
            unit,
            dydt,
            panel_type_enum,
            lineWidth,
            fillOpacity,
            showPoints,
            stacking,
            extraJson)

        # add the new panel as a new Row
        row = Row(title=title, panels=[panel])
        self.rows.append(row)
        self.current_y += self.panel_height   

    def AddPanelToRow(
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
        extraJson=None,
    ):
        '''
        Add panel to latest defined row
        
        :param title: panel title
        :param queries: Description
        :type queries: list[ExpressionAndLegendPair] 
        :param unit: Y-axis unit/format 'percent' , 'bytes/sec', 'short'
        :param dydt: if true aluto-generates two targets per query
        :param panel_type_enum: panel visualization PanelType.TIME_SERIES , PanelType.GAUGE , PanelType.BARGAUGE , PanelType.STAT
        :param lineWidth: line thickness 1-10
        :param fillOpacity: area fill transparency 0.0-1.0
        :param showPoints: point visibility "never" , "auto" , "always"
        :param stacking: stacking mode "off" , "normal" , "100%"
        :param extraJson: dict of raw JSON for panel constructor
        '''
        if not self.rows:
            raise ValueError("No rows defined for this dashboard")

        panel = self.CreatePanel(
            title,
            queries,
            unit,
            dydt,
            panel_type_enum,
            lineWidth,
            fillOpacity,
            showPoints,
            stacking,
            extraJson)

        self.rows[-1].panels.append(panel) 
        self.current_x += self.panel_width
        if self.current_x >= self.MAX_WIDTH:
            self.current_y += self.panel_height
            self.current_x = 0
    
    def Render(self):
        valid_rows = [r for r in self.rows if r.panels]
        return Dashboard(
            title=self.title,
            rows=valid_rows,
            timezone="browser",
            templating=Templating(list=self.templates),
        ).auto_panel_ids()
