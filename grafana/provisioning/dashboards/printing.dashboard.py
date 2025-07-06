from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import PERCENT_UNIT, SECONDS 

from common import PROMETHEUS_DATASOURCE_NAME
from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair


wrapper = SceGrafanalibWrapper("Quasar")

wrapper.DefineRow("Printer Metrics")

wrapper.AddPanel(
    title="Ink Level",
    queries=[
        ExpressionAndLegendPair(
            'snmp_metric{name="ink_level",ip="192.168.69.149"} / ignoring(name) group_left() snmp_metric{name="ink_capacity",ip="192.168.69.149"}',
            "Left Printer {{ip}}"
        ),
        ExpressionAndLegendPair(
            'snmp_metric{name="ink_level",ip="192.168.69.208"} / ignoring(name) group_left() snmp_metric{name="ink_capacity",ip="192.168.69.208"}',
            "Right Printer {{ip}}"
        )
    ],
    unit=PERCENT_UNIT,
    dydt=False
)

wrapper.AddPanel(
    title="# of Pages Printed",
    queries=[
        ExpressionAndLegendPair(
            'snmp_metric{name="page_count"}',
            "{{ip}}"
        )
    ],
    unit="",
    dydt=True
)

wrapper.DefineRow("SNMP Metrics")

wrapper.AddPanel(
    title="SNMP Request Duration",
    queries=[
        ExpressionAndLegendPair(
            'snmp_request_duration_sum/snmp_request_duration_count',
            "__auto"
        )
    ],
    unit=SECONDS,
    dydt=False
)

wrapper.AddPanel(
    title="Print Jobs Received",
    queries=[
        ExpressionAndLegendPair(
            'rate(print_jobs_recieved_total[$__rate_interval])',
            "__auto"
        )
    ],
    unit="",
    dydt=False
)

wrapper.DefineRow("Error Monitoring")

wrapper.AddPanel(
    title="Active SNMP Errors",
    queries=[
        ExpressionAndLegendPair(
            'snmp_error == 1',
            "{{ip}} {{name}}"
        )
    ],
    unit="",
    dydt=False
)

dashboard = wrapper.Render()
