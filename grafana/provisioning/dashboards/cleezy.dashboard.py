from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

wrapper = SceGrafanalibWrapper(title='Cleezy')

wrapper.AddPanel(
    title="Cache Size (entries)",
    queries=[
        ExpressionAndLegendPair(
            'cache_size',
        )
    ],
)

wrapper.AddPanel(
    title="SQLite latency by query",
    queries=[
        ExpressionAndLegendPair(
            'query_time_sum / query_time_count',
            "{{query_type}}",
        )
 ],
)

wrapper.AddPanel(
    title="SQLite latency by query",
    queries=[
        ExpressionAndLegendPair(
            'http_code_total{path!="/metrics", job="cleezy"}',
            "{{code}} {{path}}",
        )
 ],
)

wrapper.AddPanel(
    title="Cache hits and misses",
    queries=[
        ExpressionAndLegendPair(
            'cache_hits_total',
        )
    ],
)

wrapper.AddPanel(
    title="Container Uptime",
    queries=[
        ExpressionAndLegendPair(
            'time() - process_start_time_seconds{job="cleezy"}',
        )
    ],
)

dashboard = wrapper.Render()
