from wrapper import DashboardWrapper
from grafanalib.core import (
    Dashboard,
    TimeSeries,
    Target,
    Stat,
    GridPos,
)
# see https://github.com/weaveworks/grafanalib/blob/main/grafanalib/formatunits.py
from grafanalib.formatunits import (
    SECONDS,
    NUMBER_FORMAT,
    BYTES,
    BITS_SEC,
)

PROMETHEUS_DATASOURCE_NAME = 'Prometheus'


dashboard = DashboardWrapper(
    title="wrapper generated",
    description="this dashboard was generated using the wrapper",
).add_panel(TimeSeries(
    title='CPU Usage',
    unit=NUMBER_FORMAT,
    gridPos=GridPos(h=8, w=12, x=0, y=0),
    lineWidth=2,
    targets=[
        Target(
            datasource=PROMETHEUS_DATASOURCE_NAME,
            expr='rate(process_cpu_seconds_total[1m])',
            refId='A',
        ),
    ],
)).generate().auto_panel_ids()
