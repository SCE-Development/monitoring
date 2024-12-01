from grafanalib.core import (
    Dashboard, TimeSeries, GaugePanel,
    Target, GridPos,
    OPS_FORMAT, Templating, Template, REFRESH_ON_TIME_RANGE_CHANGE, Logs
)
from grafanalib.formatunits import BYTES_IEC, SECONDS, BYTES_SEC_IEC

from common import PROMETHEUS_DATASOURCE_NAME


dashboard = Dashboard(
    title='Cadvisor',
    uid='cadvisor',
    description='Container metrics collected by Cadvisor',
    tags=[
        'linux',
        'docker',
    ],
    templating=Templating(list=[
        Template(
            name='compose_project',
            label='Compose Project',
            dataSource=PROMETHEUS_DATASOURCE_NAME,
            query='label_values({__name__=~"container.*"}, container_label_com_docker_compose_project)',
            includeAll=True,
            multi=True,
            refresh=REFRESH_ON_TIME_RANGE_CHANGE,
        ),
        Template(
            name='container_name',
            label='Container',
            dataSource=PROMETHEUS_DATASOURCE_NAME,
            query='label_values({__name__=~"container.*", container_label_com_docker_compose_project=~"$compose_project"}, name)',
            includeAll=True,
            multi=True,
            refresh=REFRESH_ON_TIME_RANGE_CHANGE,
        ),
    ]),
    timezone='browser',
    panels=[
        TimeSeries(
            title='Container Memory Usage',
            unit=BYTES_IEC,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=2,
            fillOpacity=10,
            showPoints='never',
            stacking={'mode': 'normal'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='max by (name) (container_memory_usage_bytes{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"})',
                    legendFormat='{{ name }}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Container CPU Usage',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            lineWidth=2,
            fillOpacity=10,
            showPoints='never',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='max by (name) (rate(container_cpu_usage_seconds_total{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
                    legendFormat='{{ name }}',
                    refId='A',
                ),
            ],
        ),
        TimeSeries(
            title='Container Network Traffic',
            unit=BYTES_SEC_IEC,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            lineWidth=2,
            fillOpacity=10,
            showPoints='never',
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='max by (name) (rate(container_network_receive_bytes_total{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
                    legendFormat="rx {{ name }}",
                    refId='A',
                ),
                Target(
                    datasource=PROMETHEUS_DATASOURCE_NAME,
                    expr='-max by (name) (rate(container_network_transmit_bytes_total{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
                    legendFormat="tx {{ name }}",
                    refId='B',
                ),
            ],
        ),
    ],
).auto_panel_ids()
