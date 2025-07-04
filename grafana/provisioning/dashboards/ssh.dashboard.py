from grafanalib.core import Dashboard, Templating, Stat, TimeSeries, Target, GridPos
from grafanalib.formatunits import SECONDS, TRUE_FALSE, DAYS

from common import PROMETHEUS_DATASOURCE_NAME
from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

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

wrapper = SceGrafanalibWrapper("SSH Tunnel Health")

wrapper.DefineRow("Health Checks")

wrapper.AddPanel(
    title="Time since last health check",
    queries=[
        ExpressionAndLegendPair(
            'time() - last_health_check_request',
            "{{job}}"
        )
    ],
    unit=SECONDS,
    dydt=False
)

wrapper.AddPanel(
    title="Time since SSH tunnel reopened",
    queries=[
        ExpressionAndLegendPair(
            'time() - ssh_tunnel_last_opened',
            "{{job}}"
        )
    ],
    unit=SECONDS,
    dydt=False
)

wrapper.DefineRow("Container Status")

wrapper.AddPanel(
    title="Container Health",
    queries=[
        ExpressionAndLegendPair(
            'up{job=~"led-sign|delen|sce-printer"}',
            "{{job}}"
        ),
        ExpressionAndLegendPair(
            'up{instance="prometheus-clark-sshtunnel:9090"}',
            "{{job}}"
        )
    ],
    unit=TRUE_FALSE,
    dydt=False
)

wrapper.AddPanel(
    title="Container Uptime",
    queries=[
        ExpressionAndLegendPair(
            'time() - process_start_time_seconds{job=~"led-sign|delen|sce-printer"}',
            "{{job}}"
        )
    ],
    unit=SECONDS,
    dydt=False
)

dashboard = wrapper.Render()
