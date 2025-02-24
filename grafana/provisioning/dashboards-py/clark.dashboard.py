from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE

from common import PROMETHEUS_DATASOURCE_NAME


dashboard = Dashboard(
    title='Clark',
    uid='clark',
    description='sce club website',
    timezone='browser',
    panels=[
        TimeSeries(
            title='All main-endpoints traffic',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='endpoint_hits{route!="/metrics"}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Account access',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='endpoint_hits{route=~"/(validateVerificationEmail|sendPasswordReset|validatePasswordReset|resetPassword)"}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Office Access Card',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='endpoint_hits{route=~"/(verify)"}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Messaging',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=12, y=8),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='endpoint_hits{route=~"/(send|listen|getLatestMessage)"}',
                    refId='A',
                ),
            ],
        ),
    ],
).auto_panel_ids()
