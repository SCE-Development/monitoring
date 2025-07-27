from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair, PanelType
from grafanalib.formatunits import PERCENT_UNIT, SECONDS

dashboard_wrapper = SceGrafanalibWrapper(title="Quasar")

dashboard_wrapper.AddPanel(
    title="Ink Level",
    unit=PERCENT_UNIT,
    queries=[
        ExpressionAndLegendPair(
            expression='snmp_metric{name="ink_level",ip="192.168.69.149"} / ignoring(name) group_left() snmp_metric{name="ink_capacity",ip="192.168.69.149"}',
            legend='Left Printer {{ip}}'
        ),
        ExpressionAndLegendPair(
            expression='snmp_metric{name="ink_level",ip="192.168.69.208"} / ignoring(name) group_left() snmp_metric{name="ink_capacity",ip="192.168.69.208"}',
            legend='Right Printer {{ip}}'
        )
    ]
)

dashboard_wrapper.AddPanel(
    title="# of Pages Printed",
    queries=[
        ExpressionAndLegendPair(
            expression='snmp_metric{name="page_count"}',
            legend='{{ip}}'
        )
    ]
)

dashboard_wrapper.AddPanel(
    title="SNMP Request Duration",
    unit=SECONDS,
    queries=[
        ExpressionAndLegendPair(
            expression='snmp_request_duration_sum/snmp_request_duration_count',
            legend='__auto'
        )
    ]
)

dashboard_wrapper.AddPanel(
    title="Print Jobs Recieved",
    queries=[
        ExpressionAndLegendPair(
            expression='rate(print_jobs_recieved_total[$__rate_interval])',
            legend='__auto'
        )
    ]
)

dashboard_wrapper.AddPanel(
    title="Active SNMP Errors",
    queries=[
        ExpressionAndLegendPair(
            expression='snmp_error == 1',
            legend='{{ip}} {{name}}'
        )
    ]
)

dashboard = dashboard_wrapper.Render()
