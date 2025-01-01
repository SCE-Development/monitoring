from grafanalib.core import Templating, Template, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE

from common import MyDashboard, MyTimeSeries, PromTarget


dashboard = MyDashboard(
    title='Clark',
    uid='clark',
    description='sce club website',
    panels=[
        MyTimeSeries(
            title='Clark main-endpoint hits',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='endpoint_hits{route!="/metrics"}',
                ),
            ],
        ),
        MyTimeSeries(
            title='Clark main-endpoint hits',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='endpoint_hits{route=~"/(sendPasswordReset|validatePasswordReset|resetPassword)"}',
                ),
            ],
        ),
        MyTimeSeries(
            title='Clark - messages',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='endpoint_hits{route=~"/(send|listen|getLatestMessage)"}',
                ),
            ],
        ),
    ],
).auto_panel_ids()
