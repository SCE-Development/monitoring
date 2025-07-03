from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair
from common import PROMETHEUS_DATASOURCE_NAME


wrapper = SceGrafanalibWrapper("Cleezy")

wrapper.DefineRow("Cache Metrics")
wrapper.AddPanel(
    title="Cache Size (entries)",
    queries=[
        ExpressionAndLegendPair(
            'cache_size',
            "",
        )
    ],
    unit=NUMBER_FORMAT,
    dydt=True
)

wrapper.AddPanel(
    title="SQLite latency by query",
    queries=[
        ExpressionAndLegendPair(
            'query_time_sum / query_time_count',
            "{{query_type}}",
        )
    ],
    unit=NUMBER_FORMAT,
    dydt=False
)

# HTTP status codes panel
wrapper.AddPanel(
    title="HTTP Status Codes",
    queries=[
        ExpressionAndLegendPair(
            'http_code_total{path!="/metrics", job="cleezy"}',
            "{{code}} {{path}}",
        )
    ],
    unit=NUMBER_FORMAT,
    dydt=True
)

wrapper.AddPanel(
    title="Cache hits and misses",
    queries=[
        ExpressionAndLegendPair(
            'cache_hits_total',
            "{{__name__}}",
        )
    ],
    unit=NUMBER_FORMAT,
    dydt=True
)

wrapper.AddPanel(
    title="Container Uptime",
    queries=[
        ExpressionAndLegendPair(
            'time() - process_start_time_seconds{job="cleezy"}',
            "",
        )
    ],
    unit=NUMBER_FORMAT,
    dydt=False
)

dashboard = wrapper.Render()
