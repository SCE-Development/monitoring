from grafanalib.core import (
    Dashboard,
    Templating,
    Template,
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
    title='SCE TV',
    uid='scetv',
    description='SCE video streaming service',
    timezone='browser',
    panels=[
        BarGauge(
            title='HTTP Requests',
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='http_request_count_total{endpoint!=\"/metrics\"}',
                    legendFormat='{{endpoint}}',
                    refId='A',
                ),
            ],
        ),
        Stat(
            title='Container Uptime',
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='time() - process_start_time_seconds{job=\"sce-tv\"}',
                    legendFormat='{{job}}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Data Downloaded',
            unit=BYTES,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='data_downloaded_total',
                    legendFormat="{{job}}",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='API data rate',
            gridPos=GridPos(h=8, w=12, x=12, y=8),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            unit=BITS_SEC,
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='data_downloaded_total{job=\"sce-tv\"} * 8 / download_time_sum',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Download Time',
            gridPos=GridPos(h=8, w=12, x=0, y=16),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            unit=SECONDS
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='download_time_sum',
                    legendFormat="{{job}}",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Cache Hit/Miss',
            gridPos=GridPos(h=8, w=12, x=12, y=16),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            unit=NUMBER_FORMAT,
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='cache_miss_count_total',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Total Videos Downloaded',
            gridPos=GridPos(h=8, w=12, x=0, y=24),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            unit=NUMBER_FORMAT,
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='video_download_count_total',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Cache Size Bytes',
            gridPos=GridPos(h=8, w=12, x=0, y=24),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            unit=BYTES,
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='cache_size_bytes',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Total YouTube Videos Played',
            gridPos=GridPos(h=8, w=12, x=8, y=24),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            unit=BYTES,
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='video_count_total',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Cache Size',
            gridPos=GridPos(h=8, w=12, x=0, y=32),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            unit=NUMBER_FORMAT,
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='cache_size{job=\"sce-tv\"}',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
    ],
).auto_panel_ids()
