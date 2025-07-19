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
from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

wrapper = SceGrafanalibWrapper("SCE Infra")


wrapper.AddPanel(
    title="Container Uptime",
    queries=[
        ExpressionAndLegendPair(
            'time() - process_start_time_seconds',
            '{{job}}'
        ),
        ExpressionAndLegendPair(
            'time() - container_start_time_seconds{image=~\"clark.*|nginx|mongo\"}',
            '{{name}}'
        )
    ],
    unit=SECONDS,
    dydt=False
)

wrapper.AddPanel(
    title="Metric Health",
    queries=[
        ExpressionAndLegendPair(
            'up',
            '{{instance}}'
        )
    ], 
    unit=NUMBER_FORMAT,
    dydt=False
)




wrapper.AddPanel(
    title="Container Last Seen (Clark Only)",
    queries=[
        ExpressionAndLegendPair(
            'time() - container_last_seen{image=~\"clark.*|nginx|mongo\"}',
            '{{image}}'
        )
    ],
    unit=SECONDS,
    dydt=False
)

dashboard = wrapper.Render()

