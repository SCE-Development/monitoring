from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS, NUMBER_FORMAT, TRUE_FALSE

from common import PrometheusTemplate

dashboard = Dashboard(
    title='Printers',
    uid='printers',
    description='Printer metrics',
    timezone='browser',
    templating=Templating(list=[
        # Datasource
        PrometheusTemplate,
    ]),
    panels=[
        TimeSeries(
            title='Ink Level',
            unit=PERCENT_UNIT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            stacking={'group': 'A','mode': 'none'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='snmp_metric{name=\"ink_level\",ip=\"192.168.69.149\"} / ignoring(name) group_left() snmp_metric{name=\"ink_capacity\",ip=\"192.168.69.149\"}',
                    legendFormat='Left Printer {{ip}}',
                    refId='A',
                ),
                Target(
                    datasource='${datasource}',
                    expr='snmp_metric{name=\"ink_level\",ip=\"192.168.69.208\"} / ignoring(name) group_left() snmp_metric{name=\"ink_capacity\",ip=\"192.168.69.208\"}',
                    legendFormat='Right Printer {{ip}}',
                    refId='B',
                ),
            ],
        ),
        TimeSeries(
            title='# of Pages Printed',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='snmp_metric{name=\"page_count\"}',
                    legendFormat='{{ip}}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='SNMP Request Duration',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='snmp_request_duration_sum/snmp_request_duration_count',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Print Jobs Recieved',
            unit=NUMBER_FORMAT,
            gridPos=GridPos(h=8, w=12, x=12, y=8),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='rate(print_jobs_recieved_total[$__rate_interval])',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Error',
            unit=TRUE_FALSE,
            gridPos=GridPos(h=8, w=12, x=0, y=16),
            lineWidth=2,
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='snmp_error',
                    legendFormat="__auto",
                    refId='A',
                ),
            ],
        ),
    ],
).auto_panel_ids()