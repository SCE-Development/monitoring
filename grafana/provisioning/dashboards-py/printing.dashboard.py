from grafanalib.core import Templating, Template, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS 

from common import MyDashboard, MyTimeSeries, PromTarget


dashboard = MyDashboard(
    title='Quasar',
    uid='quasar',
    description='Printer metrics',
    panels=[
        MyTimeSeries(
            title='Ink Level',
            unit=PERCENT_UNIT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='snmp_metric{name="ink_level",ip="192.168.69.149"} / ignoring(name) group_left() snmp_metric{name="ink_capacity",ip="192.168.69.149"}',
                    legendFormat='Left Printer {{ip}}',
                ),
                PromTarget(
                    expr='snmp_metric{name="ink_level",ip="192.168.69.208"} / ignoring(name) group_left() snmp_metric{name="ink_capacity",ip="192.168.69.208"}',
                    legendFormat='Right Printer {{ip}}',
                ),
            ],
        ),
        MyTimeSeries(
            title='# of Pages Printed',
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='snmp_metric{name="page_count"}',
                    legendFormat='{{ip}}',
                ),
            ],
        ),
        MyTimeSeries(
            title='SNMP Request Duration',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='snmp_request_duration_sum/snmp_request_duration_count',
                    legendFormat="__auto",
                ),
            ],
        ),
        MyTimeSeries(
            title='Print Jobs Recieved',
            gridPos=GridPos(h=8, w=12, x=12, y=8),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='rate(print_jobs_recieved_total[$__rate_interval])',
                    legendFormat="__auto",
                ),
            ],
        ),
        MyTimeSeries(
            title='Error',
            gridPos=GridPos(h=8, w=12, x=0, y=16),
            tooltipSort='desc',
            targets=[
                PromTarget(
                    expr='snmp_error',
                    legendFormat="__auto",
                ),
            ],
        ),
    ],
).auto_panel_ids()
