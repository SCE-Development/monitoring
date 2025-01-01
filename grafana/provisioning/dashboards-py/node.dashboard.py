from grafanalib.core import Templating, Template, GridPos
from grafanalib.formatunits import BYTES_IEC, BITS_SEC, PERCENT_UNIT

from common import MyTimeSeries, MyDashboard, PromTarget, PROMETHEUS_DATASOURCE_NAME

dashboard = MyDashboard(
    title='Node Exporter',
    uid='node',
    description='Node Exporter (not quite full)',
    tags=[
        'linux',
    ],
    templating=Templating(list=[
        # Job
        Template(
            name='job',
            label='Job',
            dataSource=PROMETHEUS_DATASOURCE_NAME,
            query='label_values(node_uname_info, job)',
        ),
        # Instance
        Template(
            name='instance',
            label='Instance',
            dataSource=PROMETHEUS_DATASOURCE_NAME,
            query='label_values(node_uname_info{job="$job"}, instance)',
        ),
    ]),
    panels=[
        # CPU Basic
        MyTimeSeries(
            title='CPU Basic',
            description='Basic CPU usage info',
            unit=PERCENT_UNIT,
            gridPos=GridPos(h=8, w=12, x=0, y=0),
            stacking={'mode': 'percent'},
            targets=[
                PromTarget(
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="system"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Busy System',
                ),
                PromTarget(
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="user"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Busy User',
                ),
                PromTarget(
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="iowait"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Busy Iowait',
                ),
                PromTarget(
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode=~".*irq"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Busy IRQs',
                ),
                PromTarget(
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job",  mode!="idle",mode!="user",mode!="system",mode!="iowait",mode!="irq",mode!="softirq"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Busy Other',
                ),
                PromTarget(
                    expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="idle"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                    legendFormat='Idle',
                ),
            ],
        ),
        # Memory Basic
        MyTimeSeries(
            title='Memory Basic',
            description='Basic memory usage',
            unit=BYTES_IEC,
            gridPos=GridPos(h=8, w=12, x=12, y=0),
            stacking={'mode': 'normal'},
            valueMin=0,
            targets=[
                PromTarget(
                    expr='node_memory_MemTotal_bytes{instance="$instance",job="$job"}',
                    format='time_series',
                    legendFormat='RAM Total',
                ),
                PromTarget(
                    expr='node_memory_MemTotal_bytes{instance="$instance",job="$job"} - node_memory_MemFree_bytes{instance="$instance",job="$job"} - (node_memory_Cached_bytes{instance="$instance",job="$job"} + node_memory_Buffers_bytes{instance="$instance",job="$job"} + node_memory_SReclaimable_bytes{instance="$instance",job="$job"})',
                    format='time_series',
                    legendFormat='RAM Used',
                ),
                PromTarget(
                    expr='node_memory_Cached_bytes{instance="$instance",job="$job"} + node_memory_Buffers_bytes{instance="$instance",job="$job"} + node_memory_SReclaimable_bytes{instance="$instance",job="$job"}',
                    legendFormat='RAM Cache + Buffer',
                ),
                PromTarget(
                    expr='node_memory_MemFree_bytes{instance="$instance",job="$job"}',
                    legendFormat='RAM Free',
                ),
                PromTarget(
                    expr='(node_memory_SwapTotal_bytes{instance="$instance",job="$job"} - node_memory_SwapFree_bytes{instance="$instance",job="$job"})',
                    legendFormat='SWAP Used',
                ),
            ],
            overrides=[
                # Prevent total memory from being stacked
                {
                    'matcher': {
                        'id': 'byName',
                        'options': 'RAM Total'
                    },
                    'properties': [
                        {
                            'id': 'custom.stacking',
                            'value': {'mode': 'none'}
                        }
                    ]
                },
            ],
        ),
        # Network Traffic Basic
        MyTimeSeries(
            title='Network Traffic Basic',
            description='Basic network usage info per interface',
            unit=BITS_SEC,
            gridPos=GridPos(h=8, w=12, x=0, y=8),
            tooltipSort='desc',
            axisCenteredZero=True,
            targets=[
                PromTarget(
                    expr='irate(node_network_receive_bytes_total{instance="$instance",job="$job"}[$__rate_interval]) * 8',
                    legendFormat='rx {{ device }}',
                ),
                PromTarget(
                    expr='-irate(node_network_transmit_bytes_total{instance="$instance",job="$job"}[$__rate_interval]) * 8',
                    legendFormat='tx {{ device }}',
                ),
            ],
        ),
        # Disk Space Basic
        MyTimeSeries(
            title='Disk Space Used Basic',
            description='Disk space used of all filesystems mounted',
            unit=PERCENT_UNIT,
            gridPos=GridPos(h=8, w=12, x=12, y=8),
            targets=[
                PromTarget(
                    expr='1 - (node_filesystem_avail_bytes{instance="$instance",job="$job",device!~"rootfs"} / node_filesystem_size_bytes{instance="$instance",job="$job",device!~"rootfs"})',
                    legendFormat='{{ mountpoint }}',
                ),
            ],
        ),
    ],
).auto_panel_ids()
