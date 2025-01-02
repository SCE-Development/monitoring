from grafanalib.core import GridPos, Templating, Template, Logs
from grafanalib.formatunits import BYTES_IEC, SECONDS, BYTES_SEC_IEC

from common import PROMETHEUS_DATASOURCE_NAME, MyDashboard, MyTimeSeries, PromTarget

dashboard = MyDashboard(
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
        ),
        Template(
            name='container_name',
            label='Container',
            dataSource=PROMETHEUS_DATASOURCE_NAME,
            query='label_values({__name__=~"container.*", container_label_com_docker_compose_project=~"$compose_project"}, name)',
            includeAll=True,
            multi=True,
        ),
    ]),
    panels=[
        MyTimeSeries(
            title='Container Memory Usage',
            unit=BYTES_IEC,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            tooltipSort='desc',
            stacking={'mode': 'normal'},
            targets=[
                PromTarget(
                    expr='max by (name) (container_memory_usage_bytes{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"})',
                    legendFormat='{{ name }}',
                ),
            ],
        ),
        MyTimeSeries(
            title='Container CPU Usage',
            unit=SECONDS,
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            tooltipSort='desc',
            stacking={'mode': 'normal'},
            targets=[
                PromTarget(
                    expr='max by (name) (irate(container_cpu_usage_seconds_total{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
                    legendFormat='{{ name }}',
                ),
            ],
        ),
        MyTimeSeries(
            title='Container Network Traffic',
            unit=BYTES_SEC_IEC,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            tooltipSort='desc',
            axisCenteredZero=True,
            targets=[
                PromTarget(
                    expr='max by (name) (irate(container_network_receive_bytes_total{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
                    legendFormat="rx {{ name }}",
                ),
                PromTarget(
                    expr='-max by (name) (irate(container_network_transmit_bytes_total{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"}[$__rate_interval]))',
                    legendFormat="tx {{ name }}",
                ),
            ],
        ),
    ],
).auto_panel_ids()
