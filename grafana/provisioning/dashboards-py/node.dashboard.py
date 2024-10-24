from grafanalib.core import Dashboard, Templating, Template, TimeSeries, PERCENT_UNIT_FORMAT, GridPos, Target
from grafanalib.formatunits import BYTES_IEC

from common import PrometheusTemplate
from node_consts import CPU_BASIC_COLORS, MEMORY_BASIC_COLORS

dashboard = Dashboard(
    title='Node Exporter',
    uid='node',
    description='Node Exporter (not quite full)',
    tags=[
        'linux',
    ],
    timezone='browser',
    templating=Templating(list=[
        # Datasource
        PrometheusTemplate,
        # Job
        Template(
            name='job',
            label='Job',
            dataSource='${datasource}',
            query='label_values(node_uname_info, job)',
        ),
        # Instance
        Template(
            name='instance',
            label='Instance',
            dataSource='${datasource}',
            query='label_values(node_uname_info{job="$job"}, instance)',
        ),
    ]),
    panels=[
        # CPU Basic
        TimeSeries(
            title='CPU Basic',
            description='Basic CPU usage info',
            unit=PERCENT_UNIT_FORMAT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            lineWidth=1,
            fillOpacity=30,
            showPoints='never',
            stacking={'mode': 'percent', 'group': 'A'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="system"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Busy System',
                    refId='A',
                ),
                Target(
                    datasource='${datasource}',
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="user"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Busy User',
                    refId='B',
                ),
                Target(
                    datasource='${datasource}',
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="iowait"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Busy Iowait',
                    refId='C',
                ),
                Target(
                    datasource='${datasource}',
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode=~".*irq"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Busy IRQs',
                    refId='D',
                ),
                Target(
                    datasource='${datasource}',
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job",  mode!="idle",mode!="user",mode!="system",mode!="iowait",mode!="irq",mode!="softirq"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Busy Other',
                    refId='E',
                ),
                Target(
                    datasource='${datasource}',
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="idle"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Idle',
                    refId='F',
                ),
            ],
            # Extra JSON for the colors
            extraJson=CPU_BASIC_COLORS,
        ),
        # Memory Basic
        TimeSeries(
            title='Memory Basic',
            description='Basic memory usage',
            unit=BYTES_IEC,
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            lineWidth=1,
            fillOpacity=30,
            showPoints='never',
            stacking={'mode': 'normal', 'group': 'A'},
            tooltipMode='all',
            tooltipSort='desc',
            targets=[
                Target(
                    datasource='${datasource}',
                    expr='node_memory_MemTotal_bytes{instance="$instance",job="$job"}',
                    format='time_series',
                    legendFormat='RAM Total',
                    refId='A',
                ),
                Target(
                    datasource='${datasource}',
                    expr='node_memory_MemTotal_bytes{instance="$instance",job="$job"} - node_memory_MemFree_bytes{instance="$instance",job="$job"} - (node_memory_Cached_bytes{instance="$instance",job="$job"} + node_memory_Buffers_bytes{instance="$instance",job="$job"} + node_memory_SReclaimable_bytes{instance="$instance",job="$job"})',
                    format='time_series',
                    legendFormat='RAM Used',
                    refId='B',
                ),
                Target(
                    datasource='${datasource}',
                    expr='node_memory_Cached_bytes{instance="$instance",job="$job"} + node_memory_Buffers_bytes{instance="$instance",job="$job"} + node_memory_SReclaimable_bytes{instance="$instance",job="$job"}',
                    legendFormat='RAM Cache + Buffer',
                    refId='C',
                ),
                Target(
                    datasource='${datasource}',
                    expr='node_memory_MemFree_bytes{instance="$instance",job="$job"}',
                    legendFormat='RAM Free',
                    refId='D',
                ),
                Target(
                    datasource='${datasource}',
                    expr='(node_memory_SwapTotal_bytes{instance="$instance",job="$job"} - node_memory_SwapFree_bytes{instance="$instance",job="$job"})',
                    legendFormat='SWAP Used',
                    refId='E',
                ),
            ],
            # Extra JSON for the colors
            extraJson=MEMORY_BASIC_COLORS,
        ),
        # TODO: Network Basic
        # TODO: Disk Basic
    ],
).auto_panel_ids()
