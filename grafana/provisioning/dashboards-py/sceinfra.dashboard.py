from grafanalib.core import (
    Dashboard,
    Templating,
    Template,
    Threshold,
    TimeSeries,
    Target,
    GridPos,
    BarGauge,
    Stat,
)
# see https://github.com/weaveworks/grafanalib/blob/main/grafanalib/formatunits.py
from grafanalib.formatunits import (
    PERCENT_UNIT,
    SECONDS,
    NUMBER_FORMAT,
    BYTES,
    BITS_SEC,
)

from common import PROMETHEUS_DATASOURCE_NAME


dashboard = Dashboard(
    title='SCE Infra',
    uid='sceinfra',
    description='SCE services',
    timezone='browser',
    panels=[
        Stat(
            title='Container Uptime',
            reduceCalc='lastNotNull',
            gridPos=GridPos(h=16, w=24, x=0, y=0),
            thresholds=[
                Threshold('green', 0, 0.0),
            ],
            format=SECONDS,
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='time() - process_start_time_seconds',
                    legendFormat='{{job}}',
                    refId='A',
                ),
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='time() - container_start_time_seconds{image=~\"clark.*|nginx|mongo\"}',
                    legendFormat='{{name}}',
                    refId='B',
                ),
            ],
        ),
        TimeSeries(
            title='Metric Health',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=16),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='up',
                    legendFormat="{{instance}}",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Container Last Seen (Clark Only)',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=12, y=16),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='time() - container_last_seen{image=~\"clark.*|nginx|mongo\"}',
                    legendFormat="{{image}}",
                    refId='A',
                ),
            ],
        ),
    ],
).auto_panel_ids()
