from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE


dashboard = Dashboard(
    title='Clark',
    uid='clark',
    description='sce club website',
    timezone='browser',
    panels=[
        TimeSeries(
            title='Clark main-endpoint hits',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='endpoint_hits{route!="/metrics"}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Clark main-endpoint hits',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='endpoint_hits{route=~"/(sendPasswordReset|validatePasswordReset|resetPassword)"}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Clark - messages',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='endpoint_hits{route=~"/(send|listen|getLatestMessage)"}',
                    refId='A',
                ),
            ],
        ),
    ],
).auto_panel_ids()
