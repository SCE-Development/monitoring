from grafanalib.core import (
    Dashboard, TimeSeries, GaugePanel,
    Target, GridPos,
    OPS_FORMAT, Templating, Template, REFRESH_ON_TIME_RANGE_CHANGE
)
from grafanalib.formatunits import BYTES_IEC

prom_datasource="PBFA97CFB590B2093"

dashboard = Dashboard(
    title="Containers",
    description="Data for compose projects from default Prometheus datasource collected by Cadvisor",
    tags=[
        'example'
    ],
    templating=Templating(list=[
        # TODO: test how much of this is actually necessary
        Template(
            name="compose_project",
            label="compose_project",
            dataSource=prom_datasource,
            query='label_values({__name__=~"container.*"}, container_label_com_docker_compose_project)',
            includeAll=True,
            multi=True,
            hide=0,
            sort=1,
            type="query",
            refresh=REFRESH_ON_TIME_RANGE_CHANGE,
        ),
        Template(
            name="container_name",
            label="container_name",
            dataSource=prom_datasource,
            query='label_values({__name__=~"container.*", container_label_com_docker_compose_project=~"$compose_project"}, name)',
            includeAll=True,
            multi=True,
            hide=0,
            sort=1,
            type="query",
            refresh=REFRESH_ON_TIME_RANGE_CHANGE,

        ),
    ]),
    timezone="browser",
    panels=[
        TimeSeries(
            title="Container Memory Usage",
            targets=[
                Target(
                    datasource=prom_datasource,
                    expr='max by (name) (container_memory_usage_bytes{name=~"$container_name", container_label_com_docker_compose_project=~"$compose_project"})',
                    legendFormat="{{ name }}",
                    refId='A',
                ),
            ],
            unit=BYTES_IEC,
            gridPos=GridPos(h=8, w=16, x=0, y=0),
        ),
    ],
).auto_panel_ids()

