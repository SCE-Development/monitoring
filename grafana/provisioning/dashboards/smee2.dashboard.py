from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

wrapper = SceGrafanalibWrapper(title='smee2')

wrapper.AddPanel(
    title="# Connected Clients",
    queries=[
        ExpressionAndLegendPair(
            'connected_clients',
        )
    ],
)

wrapper.AddPanel(
    title="Failed Websocket Connections",
    queries=[
        ExpressionAndLegendPair(
            'failed_connections',
            "{{subscription_id}} {{reason}}",
        )
 ],
)

dashboard = wrapper.Render()
