from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT

from common import PROMETHEUS_DATASOURCE_NAME


dashboard = Dashboard(
    title='SCEta',
    uid='sceta',
    description='Transit prediction service metrics',
    timezone='browser',
    panels=[
        TimeSeries(
            title='Cache Update Errors',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='cache_update_errors_total',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='HTTP Response Codes',
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            unit=NUMBER_FORMAT,
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='http_code_total{job=\"sceta-server\", path!=\"/metrics\"}',
                    legendFormat='{{code}} {{path}}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Cache Age',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='time() - cache_last_updated',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='511 API Response Codes',
            gridPos=GridPos(h=8, w=12, x=12, y=8),
            unit=NUMBER_FORMAT,
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='api_response_codes_total',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='511 API Latency',
            gridPos=GridPos(h=8, w=12, x=0, y=16),
            unit=SECONDS,
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='api_latency_sum / api_latency_count',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
    ],
).auto_panel_ids()
