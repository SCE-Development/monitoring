from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import SECONDS, NUMBER_FORMAT

from common import PrometheusTemplate

dashboard = Dashboard(
    title='SCEta',
    uid='sceta',
    description='SCEta metrics',
    timezone='browser',
    templating=Templating(list=[
        # Datasource
        PrometheusTemplate,
    ]),
    panels=[
        TimeSeries(
            title='Cache Updated Errors',
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='cache_update_errors_total',
                    legendFormat='__auto',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='HTTP Response Codes',
            desc='excluding /metrics',
            gridPos=GridPos(h=9, w=12, x=12, y=0),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='http_code_total{job=\"sceta-server\", path!=\"/metrics\"}',
                    legendFormat='{{code}} {{path}}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Cache Age',
            unit=SECONDS,
            gridPos=GridPos(h=9, w=12, x=0, y=8),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='time() - cache_last_updated',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='511 API Response Codes',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=12, y=9),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='api_response_codes_total',
                    legendFormat="bits/sec",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='511 API Latency',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=0, y=17),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='api_latency_sum / api_latency_count',
                    legendFormat='__auto',
                    refId='A',
                ),
            ],
        ),
    ],
).auto_panel_ids()
