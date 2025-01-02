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
    title='SCE TV',
    uid='scetv',
    description='SCE video streaming service',
    panels=[
        BarGauge(
            title='HTTP Requests',
            calc='lastNotNull',
            thresholds=[
                Threshold('green', 0, 0.0),
            ],
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            targets=[
                PromTarget(
                    expr='http_request_count_total{endpoint!="/metrics"}',
                    legendFormat='{{endpoint}}',
                ),
            ],
        ),
        Stat(
            title='Container Uptime',
            reduceCalc='lastNotNull',
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            thresholds=[
                Threshold('green', 0, 0.0),
            ],
            format=SECONDS,
            targets=[
                PromTarget(
                    expr='time() - process_start_time_seconds{job="sce-tv"}',
                    legendFormat='{{job}}',
                ),
            ],
        ),
        MyTimeSeries(
            title='Data Downloaded',
            unit=BYTES,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='data_downloaded_total',
                    legendFormat="{{job}}",
                ),
            ],
        ),
        MyTimeSeries(
            title='API data rate',
            gridPos=GridPos(h=8, w=12, x=12, y=8),
            tooltipSort='desc',
            unit=BITS_SEC,
            targets=[
                PromTarget(
                    expr='data_downloaded_total{job="sce-tv"} * 8 / download_time_sum',
                    legendFormat="__auto",
                ),
            ],
        ),
        MyTimeSeries(
            title='Download Time',
            gridPos=GridPos(h=8, w=12, x=0, y=16),
            tooltipSort='desc',
            unit=SECONDS,
            targets=[
                PromTarget(
                    expr='download_time_sum',
                    legendFormat="{{job}}",
                ),
            ],
        ),
        MyTimeSeries(
            title='Cache Hit/Miss',
            gridPos=GridPos(h=8, w=12, x=12, y=16),
            tooltipSort='desc',
            unit=NUMBER_FORMAT,
            targets=[
                PromTarget(
                    expr='cache_miss_count_total',
                    legendFormat="__auto",
                ),
            ],
        ),
        MyTimeSeries(
            title='Total Videos Downloaded',
            gridPos=GridPos(h=8, w=12, x=0, y=24),
            tooltipSort='desc',
            unit=NUMBER_FORMAT,
            targets=[
                PromTarget(
                    expr='video_download_count_total',
                    legendFormat="__auto",
                ),
            ],
        ),
        MyTimeSeries(
            title='Cache Size Bytes',
            gridPos=GridPos(h=8, w=12, x=12, y=24),
            tooltipSort='desc',
            unit=BYTES,
            targets=[
                PromTarget(
                    expr='cache_size_bytes',
                    legendFormat="__auto",
                ),
            ],
        ),
        MyTimeSeries(
            title='Total YouTube Videos Played',
            gridPos=GridPos(h=8, w=12, x=0, y=32),
            tooltipSort='desc',
            unit=BYTES,
            targets=[
                PromTarget(
                    expr='video_count_total',
                    legendFormat="__auto",
                ),
            ],
        ),
        MyTimeSeries(
            title='Cache Size',
            gridPos=GridPos(h=8, w=12, x=12, y=32),
            tooltipSort='desc',
            unit=NUMBER_FORMAT,
            targets=[
                PromTarget(
                    expr='cache_size{job="sce-tv"}',
                    legendFormat="__auto",
                ),
            ],
        ),
    ],
).auto_panel_ids()
