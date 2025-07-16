from grafanalib.core import (
    Dashboard, TimeSeries, GaugePanel,
    Target, GridPos,
    OPS_FORMAT, Templating, Template, REFRESH_ON_TIME_RANGE_CHANGE, Logs
)
from grafanalib.formatunits import BYTES_IEC, SECONDS, BYTES_SEC_IEC

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

wrapper = SceGrafanalibWrapper(title='Cadvisor')

wrapper.DefineTemplating(
    label='Compose Project',
    query='label_values({__name__=~"container.*"}, container_label_com_docker_compose_project)',
)

wrapper.DefineTemplating(
    label='Container',
    query='label_values({__name__=~"container.*", container_label_com_docker_compose_project=~"$compose_project"}, name)',
)

wrapper.AddPanel(
    title="Container Memory Usage",
    queries=[
        ExpressionAndLegendPair(
            'max by (name) (container_memory_usage_bytes{name=~"$container", container_label_com_docker_compose_project=~"$compose_project"})',
            '{{ name }}',
        )
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=10,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Container CPU Usage",
    queries=[
        ExpressionAndLegendPair(
            'max by (name) (rate(container_cpu_usage_seconds_total{name=~"$container", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
            '{{ name }}',
        )
    ],
    unit=SECONDS,
    lineWidth=2,
    fillOpacity=10,
    showPoints='never',
)

wrapper.AddPanel(
    title="Container Network Traffic",
    queries=[
        ExpressionAndLegendPair(
            'max by (name) (rate(container_network_receive_bytes_total{name=~"$container", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
            'rx {{ name }}',
        ),
        ExpressionAndLegendPair(
            '-max by (name) (rate(container_network_transmit_bytes_total{name=~"$container", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
            'tx {{ name }}',
        )
    ],
    unit=BYTES_SEC_IEC,
    lineWidth=2,
    fillOpacity=10,
    showPoints='never',
    stacking={'mode': 'normal'},
)

dashboard = wrapper.Render()
