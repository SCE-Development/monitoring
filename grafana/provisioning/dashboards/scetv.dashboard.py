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
    Time
)
# see https://github.com/weaveworks/grafanalib/blob/main/grafanalib/formatunits.py
from grafanalib.formatunits import (
    SECONDS,
    NUMBER_FORMAT,
    BYTES,
    BITS_SEC,
    SHORT,
)

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair, PanelType

wrapper = SceGrafanalibWrapper(title='SCE TV')

wrapper.AddPanel(
    title='HTTP Requests',
    queries=[
        ExpressionAndLegendPair(
            expression='http_request_count_total{endpoint!=\"/metrics\"}',
            legend='{{endpoint}}'
    )],
    unit=NUMBER_FORMAT,
    panel_type_enum=PanelType.BARGAUGE,
    extraJson={
        'options': {
            'fieldOptions': {
                "calcs": [
                    "lastNotNull"
                ],
            },
        }
    }
)

wrapper.AddPanel(
    title='Container Uptime',
    unit=SECONDS,
    queries=[
        ExpressionAndLegendPair(
            expression='time() - process_start_time_seconds{job=\"sce-tv\"}',
            legend='{{job}}'
        )
    ],
    panel_type_enum=PanelType.STAT
)

wrapper.AddPanel(
    title='Data Downloaded',
    unit=BYTES,
    queries=[
        ExpressionAndLegendPair(
            expression='data_downloaded_total',
            legend='{{job}}'
        )
    ],
)

wrapper.AddPanel(
    title='API data rate',
    unit=BITS_SEC,
    queries=[
        ExpressionAndLegendPair(
            expression='data_downloaded_total{job="sce-tv"} * 8 / download_time_sum',
            legend='__auto'
        )
    ],
)

wrapper.AddPanel(
    title='Download Time',
    unit=SECONDS,
    queries=[
        ExpressionAndLegendPair(
            expression='download_time_sum',
            legend='{{job}}'
        )
    ],
)

wrapper.AddPanel(
    title='Cache Hit/Miss',
    unit=NUMBER_FORMAT,
    queries=[
        ExpressionAndLegendPair(
            expression='cache_miss_count_total',
            legend='__auto'
        )
    ],
)

wrapper.AddPanel(
    title='Total Videos Downloaded',
    unit=NUMBER_FORMAT,
    queries=[
        ExpressionAndLegendPair(
            expression='video_download_count_total',
            legend='__auto'
        )
    ],
)

wrapper.AddPanel(
    title='Cache Size Bytes',
    unit=BYTES,
    queries=[
        ExpressionAndLegendPair(
            expression='cache_size_bytes',
            legend='__auto'
        )
    ],
)

wrapper.AddPanel(
    title='Total YouTube Videos Played',
    unit=BYTES,
    queries=[
        ExpressionAndLegendPair(
            expression='video_count_total',
            legend='__auto'
        )
    ],
)

wrapper.AddPanel(
    title='Cache Size',
    unit=NUMBER_FORMAT,
    queries=[
        ExpressionAndLegendPair(
            expression='cache_size{job="sce-tv"}',
            legend='__auto'
        )
    ],
)

wrapper.AddPanel(
    title='SCE TV Stream State',
    unit=SHORT,
    queries=[
        ExpressionAndLegendPair(
            expression='receive_stream_running{job="sce-tv-pi"}',
            legend='{{job}}'
        ),
        ExpressionAndLegendPair(
            expression='stream_state{job="sce-tv"}',
            legend='{{video_type}}'
        ),
    ],
)

dashboard = wrapper.Render()
