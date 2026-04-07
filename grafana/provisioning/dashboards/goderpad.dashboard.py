from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import SECONDS, NUMBER_FORMAT

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair, PanelType

wrapper = SceGrafanalibWrapper(title='goderpad')


wrapper.AddPanel(
    title="Container uptime",
    queries=[
        ExpressionAndLegendPair(
            'time() - process_start_time_seconds{job="goderpad"}',
        ),
    ],
    unit=SECONDS,
    panel_type_enum=PanelType.STAT,
)

wrapper.AddPanel(
    title="Endpoint Hits",
    queries=[
        ExpressionAndLegendPair(
            'endpoint_hits{job="goderpad", path!~"/metrics|.*[.].*"}',
            "{{code}} {{path}}",
        ),
    ],
    unit=NUMBER_FORMAT,
    panel_type_enum=PanelType.BARGAUGE,
    extraJson={
        'options': {
            'fieldOptions': {
                "calcs": [
                    "lastNotNull"
                ],
            },
        }
    }
)

wrapper.AddPanel(
    title="Rooms Active",
    queries=[
        ExpressionAndLegendPair(
            'rooms_active{job="goderpad"}',
        ),
    ],
)

wrapper.AddPanel(
    title="Room Users Total",
    queries=[
        ExpressionAndLegendPair(
            'room_users_total{job="goderpad"}',
        ),
    ],
)

wrapper.AddPanel(
    title="Room Join Errors Total",
    queries=[
        ExpressionAndLegendPair(
            'room_join_errors_total{job="goderpad"}',
        ),
    ],
)

wrapper.AddPanel(
    title="Room Create Errors Total",
    queries=[
        ExpressionAndLegendPair(
            'room_create_errors_total{job="goderpad"}',
        ),
    ],
)

wrapper.AddPanel(
    title="WebSocket Upgrade Errors Total",
    queries=[
        ExpressionAndLegendPair(
            'websocket_upgrade_errors_total{job="goderpad"}',
        ),
    ],
)

wrapper.AddPanel(
    title="Document Saves Errors Total",
    queries=[
        ExpressionAndLegendPair(
            'document_saves_errors_total{job="goderpad"}',
        ),
    ],
)

wrapper.AddPanel(
    title="Room Expiry Last Run",
    queries=[
        ExpressionAndLegendPair(
            'time() - room_expiry_last_run{job="goderpad"}',
        ),
    ],
    unit=SECONDS,
    panel_type_enum=PanelType.STAT,
)

dashboard = wrapper.Render()
