from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE

from common import PrometheusTemplate

dashboard = Dashboard(
    title='Clark',
    uid='clark',
    description='sce club website',
    timezone='browser',
    templating=Templating(list=[
        # Datasource
        PrometheusTemplate,
    ]),
    panels=[
        TimeSeries(
            title='Cache Size (entries)',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='cache_size',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='SQLite latency by query',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            legendFormat="{{query_type}}",
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='query_time_sum / query_time_count',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='SQLite latency by query',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            legendFormat="{{code}} {{path}}",
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='http_code_total{path!="/metrics", job="cleezy"}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Cache hits and misses',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            legendFormat="{{__name__}}",
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='cache_hits_total',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Container Uptime',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='time() - process_start_time_seconds{job="cleezy"}',
                    refId='A',
                ),
            ],
        ),
    ],
).auto_panel_ids()
