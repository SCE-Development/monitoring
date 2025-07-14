from grafanalib.formatunits import PERCENT_UNIT, SECONDS 
from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair
from common import PROMETHEUS_DATASOURCE_NAME

new_dashboard = SceGrafanalibWrapper(
    title='Quasar'
)

new_dashboard.AddPanel('Ink Level',[
    ExpressionAndLegendPair(expression='snmp_metric{name=\"ink_level\",ip=\"192.168.69.149\"} / ignoring(name) group_left() snmp_metric{name=\"ink_capacity\",ip=\"192.168.69.149\"}', legend='Left Printer {{ip}}'),
    ExpressionAndLegendPair(expression='snmp_metric{name=\"ink_level\",ip=\"192.168.69.208\"} / ignoring(name) group_left() snmp_metric{name=\"ink_capacity\",ip=\"192.168.69.208\"}', legend='Right Printer {{ip}}',
)], unit=PERCENT_UNIT)

new_dashboard.AddPanel('# of Pages Printed',[
    ExpressionAndLegendPair(expression='snmp_metric{name=\"page_count\"}', legend='{{ip}}')
])
new_dashboard.AddPanel('SNMP Request Duration',[
    ExpressionAndLegendPair(expression='snmp_request_duration_sum/snmp_request_duration_count', legend='__auto'),
], unit=SECONDS)
new_dashboard.AddPanel('Print Jobs Recieved',[  
    ExpressionAndLegendPair(expression='rate(print_jobs_recieved_total[$__rate_interval])', legend='__auto'),
])
new_dashboard.AddPanel('Active SNMP Errors',[
    ExpressionAndLegendPair(expression='snmp_error == 1', legend='{{ip}} {{name}}'),
])