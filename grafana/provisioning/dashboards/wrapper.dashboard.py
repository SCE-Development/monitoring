from wrapper import DashboardWrapper
from grafanalib.core import (
    Dashboard,
    Stat,
)
from grafanalib.formatunits import (
    SECONDS,
    NUMBER_FORMAT,
    BYTES,
    BITS_SEC,
)

PROMETHEUS_DATASOURCE_NAME = 'Prometheus'

dashboard = DashboardWrapper(
    title="wrapper generated",
    description="this dashboard was generated using the wrapper",
).define_row("Quick") \
 .add_time_series_panel(
    title='CPU Usage',
    queries=[
        ('rate(process_cpu_seconds_total[1m])', None),
    ],
    unit=NUMBER_FORMAT,
) \
 .add_time_series_panel(
    title='Network Bytes',
    queries=[
        ('max by (name) (rate(container_network_receive_bytes_total[1m]))', 'rx {{ name }}'),
        ('-max by (name) (rate(container_network_transmit_bytes_total[1m]))', 'tx {{ name }}'),
    ],
    unit=BYTES,
) \
 .define_row("Main") \
 .add_panel(Stat(
    title='Uptime',
    format=SECONDS,
    gridPos=None,  
    targets=[
        dict(
            datasource=PROMETHEUS_DATASOURCE_NAME,
            expr='time() - process_start_time_seconds',
            refId='A',
        ),
    ],
)) \
 .render().auto_panel_ids()
