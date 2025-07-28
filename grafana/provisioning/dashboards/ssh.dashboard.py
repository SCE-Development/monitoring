from grafanalib.core import Dashboard, Templating, Stat, TimeSeries, Target, GridPos
from grafanalib.formatunits import SECONDS, TRUE_FALSE, DAYS

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair, PanelType

wrapper = SceGrafanalibWrapper(title='SSH Tunnel Health')

time_since_ssh_overrides=[
            {
                "__systemRef": "hideSeriesFrom",
                "matcher": {
                    "id": "byNames",
                    "options": {
                        "mode": "exclude",
                        "names": [
                            "sce-printer"
                        ],
                        "prefix": "All except:",
                        "readOnly": True
                    }
                },
                "properties": [
                    {
                        "id": "custom.hideFrom",
                        "value": {
                            "legend": False,
                            "tooltip": False,
                            "viz": True
                        }
                    }
                ]
            }
    ]

uptime_thresholds=[
    {
        "color": "blue",
        "value": None
    }
]

wrapper.AddPanel(
    title='Time since last health check',
    queries=[
        ExpressionAndLegendPair(
            expression='time() - last_health_check_request',
            legend='{{job}}',
    )],
    unit=SECONDS,
    showPoints='never',
)

wrapper.AddPanel(
    title='Time since SSH tunnel reopened',
    queries=[
        ExpressionAndLegendPair(
            expression='time() - ssh_tunnel_last_opened',
            legend='{{job}}',
    )],
    unit=SECONDS,
    showPoints='never',
)

wrapper.AddPanel(
    title='Container Health',
    queries=[
        ExpressionAndLegendPair(
            expression='up{job=~"led-sign|delen|sce-printer"}',
            legend='{{job}}',
        ),
        ExpressionAndLegendPair(
            expression='up{instance=\"prometheus-clark-sshtunnel:9090\"}',
            legend='{{job}}',
        )
    ],
    unit=TRUE_FALSE,
    showPoints='never',
)


wrapper.AddPanel(
    title='Container Uptime',
    queries=[
        ExpressionAndLegendPair(
            expression='time() - process_start_time_seconds{job=~\"led-sign|delen|sce-printer\"}',
            legend='{{job}}',
    )],
    panel_type_enum=PanelType.STAT,
    unit=DAYS,
)

dashboard = wrapper.Render()