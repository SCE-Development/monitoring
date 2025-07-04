from grafanalib.core import (
    Dashboard, TimeSeries, GaugePanel,
    Target, GridPos,
    OPS_FORMAT, Templating, Template, REFRESH_ON_TIME_RANGE_CHANGE, Logs
)
from grafanalib.formatunits import BYTES_IEC, SECONDS, BYTES_SEC_IEC

from common import PROMETHEUS_DATASOURCE_NAME
from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair


wrapper = SceGrafanalibWrapper("cadvisor")

wrapper.DefineRow("Container Metrics")

wrapper.AddPanel(
    title="Container Memory usage",
    queries=[ExpressionAndLegendPair(
        'max by (name) (container_memory_usage_bytes{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"})',
        '{{ name }}'
    )
    ], 
    unit=BYTES_IEC,
    dydt=False
)

wrapper.AddPanel(
    title='Container CPU usage',
    queries=[
        ExpressionAndLegendPair(
            'max by (name) (rate(container_cpu_usage_seconds_total{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
            '{{ name }}'
        )
    ],
    unit=SECONDS, 
    dydt=False
)

wrapper.AddPanel(
    title='Container Traffic Network',
    unit=BYTES_SEC_IEC,
    queries=[
        ExpressionAndLegendPair(
            'max by (name) (rate(container_network_receive_bytes_total{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
            "rx {{ name }}",
            
        )
    ]
    dydt=False
)

dashboard = wrapper.Render()
