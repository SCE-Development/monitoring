from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import NUMBER_FORMAT

from wrapper import PanelType, SceGrafanalibWrapper, ExpressionAndLegendPair

wrapper = SceGrafanalibWrapper(title='Download Monitor')

wrapper.AddPanel(
    title='Download Speed (bytes/second)',
    unit=NUMBER_FORMAT,
    queries=[
        ExpressionAndLegendPair(
            expression="download_speed",
            legend="{{reason}}"
        )
    ],
    panel_type_enum=PanelType.TIME_SERIES
)

wrapper.AddPanel(
    title="Download Success (1=success, 0=fail)",
    unit=NUMBER_FORMAT,
    queries=[
        ExpressionAndLegendPair(
            expression="download_success",
            legend="{{reason}}"
        )
    ],
    panel_type_enum=PanelType.TIME_SERIES
)

dashboard = wrapper.Render()