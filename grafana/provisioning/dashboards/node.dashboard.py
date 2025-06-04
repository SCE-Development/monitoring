from grafanalib.core import Dashboard, Templating, Template, TimeSeries, GridPos, Target, Row, GaugePanel
from grafanalib.formatunits import BYTES_IEC, PERCENT_UNIT, BYTES_SEC_IEC

from common import PROMETHEUS_DATASOURCE_NAME
from node_consts import CPU_BASIC_COLORS, MEMORY_BASIC_COLORS, GAUGE_CONFIGS 

def create_gauge_panel(config):
    """Create a GaugePanel from a configuration dictionary."""
    return GaugePanel(
        title=config['title'],
        description=config['description'],
        gridPos=GridPos(h=4, w=3, x=config['x_pos'], y=1),
        format='percent',
        decimals=1,
        min=0,
        max=100,
        thresholdType='absolute',
        thresholds=[
            {"color": "rgba(50, 172, 45, 0.97)", "value": None},
            {"color": "rgba(237, 129, 40, 0.89)", "value": config['thresholds'][0]},
            {"color": "rgba(245, 54, 54, 0.9)", "value": config['thresholds'][1]}
        ],
        calc='lastNotNull',
        targets=[
            Target(
                datasource=PROMETHEUS_DATASOURCE_NAME,
                expr=config['expr'],
                format='time_series',
                instant=True,
                refId='A'
            )
        ]
    )

dashboard = Dashboard(
    title='Node Exporter',
    uid='node',
    description='Node Exporter (not quite full)',
    tags=[
        'linux',
    ],
    timezone='browser',
    templating=Templating(list=[
        Template(
            name='job',
            label='Job',
            dataSource=PROMETHEUS_DATASOURCE_NAME,
            query='label_values(node_uname_info, job)',
        ),
        Template(
            name='instance',
            label='Instance',
            dataSource=PROMETHEUS_DATASOURCE_NAME,
            query='label_values(node_uname_info{job="$job"}, instance)',
        ),
    ]),
    rows=[
        Row(
            title='Quick CPU / Mem / Disk',
            panels=[create_gauge_panel(config) for config in GAUGE_CONFIGS],
        ),
        Row(
            title='Basic CPU / Mem / Net / Disk',
            panels=[
                # CPU Basic
                TimeSeries(
                    title='CPU Basic',
                    description='Basic CPU usage info',
                    unit=PERCENT_UNIT,
                    gridPos=GridPos(h=8, w=12, x=0, y=0),
                    lineWidth=1,
                    fillOpacity=30,
                    showPoints='never',
                    stacking={'mode': 'percent', 'group': 'A'},
                    tooltipMode='all',
                    tooltipSort='desc',
                    targets=[
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="system"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                            legendFormat='Busy System',
                            refId='A',
                        ),
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="user"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                            legendFormat='Busy User',
                            refId='B',
                        ),
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="iowait"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                            legendFormat='Busy Iowait',
                            refId='C',
                        ),
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode=~".*irq"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                            legendFormat='Busy IRQs',
                            refId='D',
                        ),
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='sum(irate(node_cpu_seconds_total{instance="$instance",job="$job",  mode!="idle",mode!="user",mode!="system",mode!="iowait",mode!="irq",mode!="softirq"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
                            legendFormat='Busy Other',
                            refId='E',
                        ),
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
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
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='node_memory_MemTotal_bytes{instance="$instance",job="$job"}',
                            format='time_series',
                            legendFormat='RAM Total',
                            refId='A',
                        ),
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='node_memory_MemTotal_bytes{instance="$instance",job="$job"} - node_memory_MemFree_bytes{instance="$instance",job="$job"} - (node_memory_Cached_bytes{instance="$instance",job="$job"} + node_memory_Buffers_bytes{instance="$instance",job="$job"} + node_memory_SReclaimable_bytes{instance="$instance",job="$job"})',
                            format='time_series',
                            legendFormat='RAM Used',
                            refId='B',
                        ),
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='node_memory_Cached_bytes{instance="$instance",job="$job"} + node_memory_Buffers_bytes{instance="$instance",job="$job"} + node_memory_SReclaimable_bytes{instance="$instance",job="$job"}',
                            legendFormat='RAM Cache + Buffer',
                            refId='C',
                        ),
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='node_memory_MemFree_bytes{instance="$instance",job="$job"}',
                            legendFormat='RAM Free',
                            refId='D',
                        ),
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='(node_memory_SwapTotal_bytes{instance="$instance",job="$job"} - node_memory_SwapFree_bytes{instance="$instance",job="$job"})',
                            legendFormat='SWAP Used',
                            refId='E',
                        ),
                    ],
                    # Extra JSON for the colors
                    extraJson=MEMORY_BASIC_COLORS,
                    ),
                # Network Basic
                TimeSeries(
                    title='Network Traffic',
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
                            expr='rate(node_network_receive_bytes_total{instance="$instance",job="$job",device!="lo"}[$__rate_interval])',
                            legendFormat="rx {{ device }}",
                            refId='A',
                        ),
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='-rate(node_network_transmit_bytes_total{instance="$instance",job="$job",device!="lo"}[$__rate_interval])',
                            legendFormat="tx {{ device }}",
                            refId='B',
                        ),
                    ],
                ),
                # TODO: Disk Basic
            ],
        )
    ]
).auto_panel_ids()
