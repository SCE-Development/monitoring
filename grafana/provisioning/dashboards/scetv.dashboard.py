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


wrapper = SceGrafanalibWrapper("SCE TV")

wrapper.DefineRow("Service Overview")

wrapper.AddPanel(
    title="HTTP Requests",
    queries=[
        ExpressionAndLegendPair(
            'http_request_count_total{endpoint!="/metrics"}',
            "{{endpoint}}"
        )
    ],
    unit="",
    dydt=True
)

wrapper.AddPanel(
    title="Container Uptime",
    queries=[
        ExpressionAndLegendPair(
            'time() - process_start_time_seconds{job="sce-tv"}',
            "{{job}}"
        )
    ],
    unit=SECONDS,
    dydt=False
)

wrapper.DefineRow("Data Metrics")

wrapper.AddPanel(
    title="Data Downloaded",
    queries=[
        ExpressionAndLegendPair(
            'data_downloaded_total',
            "{{job}}"
        )
    ],
    unit=BYTES,
    dydt=True
)

wrapper.AddPanel(
    title="API data rate",
    queries=[
        ExpressionAndLegendPair(
            'data_downloaded_total{job="sce-tv"} * 8 / download_time_sum',
            "__auto"
        )
    ],
    unit=BITS_SEC,
    dydt=False
)

wrapper.DefineRow("Performance Metrics")

wrapper.AddPanel(
    title="Download Time",
    queries=[
        ExpressionAndLegendPair(
            'download_time_sum',
            "{{job}}"
        )
    ],
    unit=SECONDS,
    dydt=False
)

wrapper.AddPanel(
    title="Cache Hit/Miss",
    queries=[
        ExpressionAndLegendPair(
            'cache_miss_count_total',
            "__auto"
        )
    ],
    unit=NUMBER_FORMAT,
    dydt=True
)

wrapper.DefineRow("Cache Metrics")

wrapper.AddPanel(
    title="Total Videos Downloaded",
    queries=[
        ExpressionAndLegendPair(
            'video_download_count_total',
            "__auto"
        )
    ],
    unit=NUMBER_FORMAT,
    dydt=True
)

wrapper.AddPanel(
    title="Cache Size Bytes",
    queries=[
        ExpressionAndLegendPair(
            'cache_size_bytes',
            "__auto"
        )
    ],
    unit=BYTES,
    dydt=False
)

wrapper.DefineRow("Video Metrics")

wrapper.AddPanel(
    title="Total YouTube Videos Played",
    queries=[
        ExpressionAndLegendPair(
            'video_count_total',
            "__auto"
        )
    ],
    unit=BYTES,
    dydt=True
)

wrapper.AddPanel(
    title="Cache Size",
    queries=[
        ExpressionAndLegendPair(
            'cache_size{job="sce-tv"}',
            "__auto"
        )
    ],
    unit=NUMBER_FORMAT,
    dydt=False
)

dashboard = wrapper.Render()
