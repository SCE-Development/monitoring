from grafanalib.core import (
    Templating,
    Template,
    Threshold,
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

from common import MyDashboard, MyTimeSeries, PromTarget


dashboard = MyDashboard(
    title='SCE Infra',
    uid='sceinfra',
    description='SCE services',
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
                PromTarget(
                    expr='time() - process_start_time_seconds',
                    legendFormat='{{job}}',
                ),
                PromTarget(
                    expr='time() - container_start_time_seconds{image=~"clark.*|nginx|mongo"}',
                    legendFormat='{{name}}',
                ),
            ],
        ),
        MyTimeSeries(
            title='Metric Health',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=16),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='up',
                    legendFormat="{{instance}}",
                ),
            ],
        ),
        MyTimeSeries(
            title='Container Last Seen (Clark Only)',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=12, y=16),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='time() - container_last_seen{image=~"clark.*|nginx|mongo"}',
                    legendFormat="{{image}}",
                ),
            ],
        ),
    ],
).auto_panel_ids()
