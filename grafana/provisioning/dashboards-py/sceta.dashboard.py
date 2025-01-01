from grafanalib.core import Templating, Template, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT

from common import MyDashboard, MyTimeSeries, PromTarget


dashboard = MyDashboard(
    title='SCEta',
    uid='sceta',
    description='Transit prediction service metrics',
    panels=[
        MyTimeSeries(
            title='Cache Update Errors',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='cache_update_errors_total',
                    legendFormat="__auto",
                ),
            ],
        ),
        MyTimeSeries(
            title='HTTP Response Codes',
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            unit=NUMBER_FORMAT,
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='http_code_total{job="sceta-server", path!="/metrics"}',
                    legendFormat='{{code}} {{path}}',
                ),
            ],
        ),
        MyTimeSeries(
            title='Cache Age',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='time() - cache_last_updated',
                    legendFormat="__auto",
                ),
            ],
        ),
        MyTimeSeries(
            title='511 API Response Codes',
            gridPos=GridPos(h=8, w=12, x=12, y=8),
            unit=NUMBER_FORMAT,
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='api_response_codes_total',
                    legendFormat="__auto",
                ),
            ],
        ),
        MyTimeSeries(
            title='511 API Latency',
            gridPos=GridPos(h=8, w=12, x=0, y=16),
            unit=SECONDS,
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='api_latency_sum / api_latency_count',
                    legendFormat="__auto",
                ),
            ],
        ),
    ],
).auto_panel_ids()
