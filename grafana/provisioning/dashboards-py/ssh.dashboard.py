from grafanalib.core import Dashboard, Templating, Stat, TimeSeries, Target, GridPos
from grafanalib.formatunits import SECONDS, TRUE_FALSE, DAYS

from common import PROMETHEUS_DATASOURCE_NAME

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

dashboard = Dashboard(
    title='SSH Tunnel Health',
    uid='sshtunnelhealth',
    description='Health of SSH Tunnel',
    timezone='browser',
    panels=[
        TimeSeries(
            title='Time since last health check',
            unit=SECONDS,
            gridPos=GridPos(h=9, w=12, x=0, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='time() - last_health_check_request',
                    legendFormat='{{job}}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Time since SSH tunnel reopened',
            unit=SECONDS,
            gridPos=GridPos(h=9, w=12, x=12, y=0),
            overrides=time_since_ssh_overrides,
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='time() - ssh_tunnel_last_opened',
                    legendFormat='{{job}}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Container Health',
            unit=TRUE_FALSE, # idk if we should have it as true/false instead of 1/0 lol
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='up{job=~"led-sign|delen|sce-printer"}',
                    legendFormat="{{job}}",
                    refId='A',
                ),
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='up{instance=\"prometheus-clark-sshtunnel:9090\"}',
                    legendFormat="{{job}}",
                    refId='B',
                ),
            ],
        ),
        Stat(
            title='Container Uptime',
            gridPos=GridPos(h=8, w=12, x=12, y=9),
            format=SECONDS,
            decimals=2,
            reduceCalc='lastNotNull',
            thresholds=uptime_thresholds,
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='time() - process_start_time_seconds{job=~\"led-sign|delen|sce-printer\"}',
                    legendFormat="{{job}}",
                    refId='A',
                ),
            ],
        ),
    ],
).auto_panel_ids()
