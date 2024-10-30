from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos, BarGauge, Stat
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE, BYTES

from common import PrometheusTemplate

dashboard = Dashboard(
    title='SCE TV',
    uid='sce tv',
    description='SCE TV metrics',
    timezone='browser',
    templating=Templating(list=[
        # Datasource
        PrometheusTemplate,
    ]),
    panels=[
        BarGauge(
            title='HTTP Requests',
            desc='Number of requests received for each endpoint',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='http_request_count_total{endpoint!=\"/metrics\"}',
                    legendFormat='{{endpoint}}',
                    refId='A',
                ),
            ],
        ),
        Stat(
            title='Container Uptime',
            unit=SECONDS,
            gridPos=GridPos(h=9, w=12, x=12, y=0),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='time() - process_start_time_seconds{job=\"sce-tv\"}',
                    legendFormat='{{job}}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Data Downloaded',
            desc='Total video data downloaded in bytes',
            unit=BYTES,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='data_downloaded_total',
                    legendFormat="{{job}}",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='API data rate',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=12, y=9),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='data_downloaded_total{job=\"sce-tv\"} * 8 / download_time_sum',
                    legendFormat="bits/sec",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Download Time',
            desc='Total time spent downloading videos in seconds',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=0, y=16),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='download_time_sum',
                    legendFormat="{{job}}",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Cache Hit/Miss',
            desc='Success/Failure in reading from cache',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=12, y=17),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='cache_hit_count_total',
                    legendFormat="cache_hit_count",
                    refId='A',
                ),
                Target(
                    datasource='${datasource}',
                    expr='cache_miss_count_total',
                    hide=False,
                    legendFormat="cache_miss_count",
                    refId='B',
                ),
            ],
        ),
        TimeSeries(
            title='Total Videos Downloaded',
            gridPos=GridPos(h=8, w=12, x=0, y=24),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='video_download_count_total',
                    legendFormat="{{job}}",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Cache Size Bytes',
            unit=BYTES,
            gridPos=GridPos(h=8, w=12, x=12, y=25),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='cache_size_bytes',
                    legendFormat="{{job}}",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Total YouTube Videos Played',
            unit=BYTES,
            gridPos=GridPos(h=8, w=12, x=0, y=32),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='video_count_total',
                    legendFormat="{{job}}",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Cache Size',
            desc='Total entries in cache',
            unit=BYTES,
            gridPos=GridPos(h=8, w=12, x=12, y=33),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='cache_size{job=\"sce-tv\"}',
                    legendFormat="{{job}}",
                    refId='A',
                ),
            ],
        ),
    ],
).auto_panel_ids()
