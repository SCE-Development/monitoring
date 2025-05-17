from dataclasses import dataclass
import typing

from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos, Row
from grafanalib.formatunits import PERCENT_UNIT, SECONDS


STARTING_CHAR_INTEGER = ord('A')
PROMETHEUS_DATASOURCE_NAME = 'Prometheus'

class RefIdGenerator:
    offset = 0
    def Next(self) -> str:
        result = chr(STARTING_CHAR_INTEGER + self.offset)
        self.offset += 1
        return result

@dataclass
class ExpressionAndLegendPair:
    expression: str
    legend: typing.Optional[str] = None

class SceGrafanalibWrapper:
    def __init__(
        self,
        title,
        description,
        timezone="browser",
        uid=None,
    ):
        self.title = title
        self.description = description
        self.timezone = timezone
        self.uid = uid
        if uid is None:
            uid = "-".join(title.split(" ")).lower()
        self.panels = []

        self.x = 0
        self.y = 0

        self.rows = []

        # rows
        # .DefineRow("title") -> pushes thing
        # .AddPanelToRow("title")
        # .AddPanelToRow("asdf")

    def DefineRow(self, title):
        self.rows.append(
            Row(title=title, panels=[]),
        )
        return self

    def AddPanelToRow(self, title, queries: list[ExpressionAndLegendPair]):
        if not self.rows:
            raise ValueError("please call .DefineRow(title) before adding a panel")
        ref_id = RefIdGenerator()
        self.rows[-1].panels.append(
            TimeSeries(
                title=title,
                unit=PERCENT_UNIT,
                gridPos=GridPos(h=8, w=12, x=self.x, y=self.y),
                lineWidth=2,
                stacking={'group': 'A','mode': 'none'},
                tooltipMode='all',
                tooltipSort='desc',
                targets=[
                    Target(
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                        expr=query.expression,
                        legendFormat=query.legend,
                        refId=ref_id.Next(),
                    )
                    for query in queries
                ],
            )
        )
        # update coordinates for the next panel to be on the next row
        # underneath
        if self.x == 12:
            self.y += 8
            self.x = 0
        # update coordinates for the next panel to be on the same row,
        # to the right of the panel we just added
        self.x += 12

    def AddPanel(self, title, queries: list[ExpressionAndLegendPair]):
        ref_id = RefIdGenerator()
        self.panels.append(
            TimeSeries(
                title=title,
                unit=PERCENT_UNIT,
                gridPos=GridPos(h=8, w=12, x=self.x, y=self.y),
                lineWidth=2,
                stacking={'group': 'A','mode': 'none'},
                tooltipMode='all',
                tooltipSort='desc',
                targets=[
                    Target(
                        datasource=PROMETHEUS_DATASOURCE_NAME,
                        expr=query.expression,
                        legendFormat=query.legend,
                        refId=ref_id.Next(),
                    )
                    for query in queries
                ],
            )
        )
        # update coordinates for the next panel to be on the next row
        # underneath
        if self.x == 12:
            self.y += 8
            self.x = 0
        # update coordinates for the next panel to be on the same row,
        # to the right of the panel we just added
        self.x += 12

    def Render(self):
        return Dashboard(
            title=self.title,
            uid=self.uid,
            description=self.description,
            timezone=self.timezone,
            panels=self.panels,
            rows=self.rows,
        ).auto_panel_ids()
