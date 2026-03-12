from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import SECONDS

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

wrapper = SceGrafanalibWrapper(title='goderpad')


wrapper.AddPanel(
    title="Container uptime",
    queries=[
        ExpressionAndLegendPair(
            'time() - process_start_time_seconds{job="goderpad-backend"}',
        ),
    ],
    unit=SECONDS,
)

wrapper.AddPanel(
    title="Endpoint Hits",
    queries=[
        ExpressionAndLegendPair(
            'endpoint_hits_total{job="goderpad-backend", path!~"/metrics|.*[.].*"}',
            "{{code}} {{path}}",
        ),
    ],
)

wrapper.AddPanel(
    title="HTTP Request Duration Seconds",
    queries=[
        ExpressionAndLegendPair(
            'http_request_duration_seconds{job="goderpad-backend"}',
            "{{code}} {{path}}",
        ),
    ],
    unit=SECONDS,
)

wrapper.AddPanel(
    title="Rooms Active",
    queries=[
        ExpressionAndLegendPair(
            'rooms_active{job="goderpad-backend"}',
        ),
    ],
)

wrapper.AddPanel(
    title="Room Users Total",
    queries=[
        ExpressionAndLegendPair(
            'room_users_total{job="goderpad-backend"}',
        ),
    ],
)

wrapper.AddPanel(
    title="Room Join Errors Total",
    queries=[
        ExpressionAndLegendPair(
            'room_join_errors_total{job="goderpad-backend"}',
        ),
    ],
)

wrapper.AddPanel(
    title="Room Create Errors Total",
    queries=[
        ExpressionAndLegendPair(
            'room_create_errors_total{job="goderpad-backend"}',
        ),
    ],
)

wrapper.AddPanel(
    title="WebSocket Upgrade Errors Total",
    queries=[
        ExpressionAndLegendPair(
            'websocket_upgrade_errors_total{job="goderpad-backend"}',
        ),
    ],
)

wrapper.AddPanel(
    title="Document Saves Errors Total",
    queries=[
        ExpressionAndLegendPair(
            'document_saves_errors_total{job="goderpad-backend"}',
        ),
    ],
)

wrapper.AddPanel(
    title="Room Expiry Last Run",
    queries=[
        ExpressionAndLegendPair(
            'room_expiry_last_run{job="goderpad-backend"}',
        ),
    ],
)

dashboard = wrapper.Render()
