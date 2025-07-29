from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS 
from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

from common import PROMETHEUS_DATASOURCE_NAME

wrapper = SceGrafanalibWrapper(title='Quasar')

wrapper.AddPanel(
    title='Ink Level',
    queries=[
        ExpressionAndLegendPair(
            'snmp_metric{name=\"ink_level\",ip=\"192.168.69.149\"} / ignoring(name) group_left() snmp_metric{name=\"ink_capacity\",ip=\"192.168.69.149\"}',
            'Left Printer {{ip}}'
        ),
        ExpressionAndLegendPair(
            'snmp_metric{name=\"ink_level\",ip=\"192.168.69.208\"} / ignoring(name) group_left() snmp_metric{name=\"ink_capacity\",ip=\"192.168.69.208\"}',
            'Right Printer {{ip}}'
        )
    ],
    unit=PERCENT_UNIT,
    dydt=False,
    lineWidth=2,
    stacking={'group': 'A','mode': 'none'},
    # tooltipMode='all',
    # tooltipSort='desc',
)

wrapper.AddPanel(
    title='# of Pages Printed',
    queries=[
        ExpressionAndLegendPair(
            'snmp_metric{name=\"page_count\"}',
            '{{ip}}',
        )
    ],
    dydt=False,
    lineWidth=2,
    # tooltipMode='all',
    # tooltipSort='desc',
)

wrapper.AddPanel(
    title='SNMP Request Duration',
    unit=SECONDS,
    queries=[
        ExpressionAndLegendPair(
            'snmp_request_duration_sum/snmp_request_duration_count',
            '__auto',
        )
    ],
    dydt=False,
    lineWidth=2,
    # tooltipMode='all',
    # tooltipSort='desc',
)

wrapper.AddPanel(
    title='Print Jobs Recieved',
    queries=[
        ExpressionAndLegendPair(
            'rate(print_jobs_recieved_total[$__rate_interval])',
            '__auto',
        )
    ],
    dydt=False,
    lineWidth=2,
    # tooltipMode='all',
    # tooltipSort='desc',
)

wrapper.AddPanel(
    title='Active SNMP Errors',
    queries=[
        ExpressionAndLegendPair(
            'snmp_error == 1',
            '{{ip}} {{name}}',
        )
    ],
    dydt=False,
    lineWidth=2,
    # tooltipMode='all',
    # tooltipSort='desc',
)

dashboard = wrapper.Render()
