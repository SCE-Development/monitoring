from grafanalib.core import Templating, Template, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE

from common import MyDashboard, MyTimeSeries, PromTarget


dashboard = MyDashboard(
    title='Cleezy',
    uid='leezy',
    description='sce club website',
    panels=[
        MyTimeSeries(
            title='Cache Size (entries)',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='cache_size',
                ),
            ],
        ),
        MyTimeSeries(
            title='SQLite latency by query',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    legendFormat="{{query_type}}",
                    expr='query_time_sum / query_time_count',
                ),
            ],
        ),
        MyTimeSeries(
            title='SQLite latency by query',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    legendFormat="{{code}} {{path}}",
                    expr='http_code_total{path!="/metrics", job="cleezy"}',
                ),
            ],
        ),
        MyTimeSeries(
            title='Cache hits and misses',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    legendFormat="{{__name__}}",
                    expr='cache_hits_total',
                ),
            ],
        ),
        MyTimeSeries(
            title='Container Uptime',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='time() - process_start_time_seconds{job="cleezy"}',
                ),
            ],
        ),
    ],
).auto_panel_ids()
