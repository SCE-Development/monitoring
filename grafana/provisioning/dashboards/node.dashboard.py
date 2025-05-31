from grafanalib.core import Dashboard, Templating, Template, TimeSeries, GridPos, Target, Row, GaugePanel
from grafanalib.formatunits import BYTES_IEC, PERCENT_UNIT, BYTES_SEC_IEC

from common import PROMETHEUS_DATASOURCE_NAME
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
            panels=[
                GaugePanel(
                    title='CPU Busy',
                    description='Overall CPU busy percentage (averaged across all cores)',
                    gridPos=GridPos(h=4, w=3, x=3, y=1),
                    format='percent',
                    decimals=1,
                    min=0,
                    max=100,
                    thresholdType='absolute',
                    thresholds=[
                        {"color": "rgba(50, 172, 45, 0.97)", "value": None},
                        {"color": "rgba(237, 129, 40, 0.89)", "value": 85},
                        {"color": "rgba(245, 54, 54, 0.9)", "value": 95}
                    ],
                    calc='lastNotNull',
                    targets=[
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle", instance="$instance", job="$job"}[$__rate_interval])))',
                            instant=True,
                            refId='A',
                        )
                    ]
                ),
                GaugePanel(
                    title='Sys Load',
                    description='System load over all CPU cores together',
                    gridPos=GridPos(h=4, w=3, x=6, y=1),
                    format='percent',
                    decimals=1,
                    min=0,
                    max=100,
                    thresholdType='absolute',
                    thresholds=[
                        {"color": "rgba(50, 172, 45, 0.97)", "value": None},
                        {"color": "rgba(237, 129, 40, 0.89)", "value": 85},
                        {"color": "rgba(245, 54, 54, 0.9)", "value": 95}
                    ],
                    calc='lastNotNull',
                    targets=[
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='scalar(node_load1{instance="$instance",job="$job"}) * 100 / count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu))',
                            format='time_series',
                            instant=True,
                            refId='A'
                        )
                    ]
                ),
                GaugePanel(
                    title='RAM Used',
                    description='Real RAM usage excluding cache and reclaimable memory',
                    gridPos=GridPos(h=4, w=3, x=9, y=1),
                    format='percent',
                    decimals=1,
                    min=0,
                    max=100,
                    thresholdType='absolute',
                    thresholds=[
                        {"color": "rgba(50, 172, 45, 0.97)", "value": None},
                        {"color": "rgba(237, 129, 40, 0.89)", "value": 80},
                        {"color": "rgba(245, 54, 54, 0.9)", "value": 90}
                    ],
                    calc='lastNotNull',
                    targets=[
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='(1 - (node_memory_MemAvailable_bytes{instance="$instance", job="$job"} / node_memory_MemTotal_bytes{instance="$instance", job="$job"})) * 100',
                            format='time_series',
                            instant=True,
                            refId='B'
                        )
                    ]
                ),
                GaugePanel(
                    title='SWAP Used',
                    description='Percentage of swap space currently used by the system',
                    gridPos=GridPos(h=4, w=3, x=12, y=1),
                    format='percent',
                    decimals=1,
                    min=0,
                    max=100,
                    thresholdType='absolute',
                    thresholds=[
                        {"color": "rgba(50, 172, 45, 0.97)", "value": None},
                        {"color": "rgba(237, 129, 40, 0.89)", "value": 10},
                        {"color": "rgba(245, 54, 54, 0.9)", "value": 25}
                    ],
                    calc='lastNotNull',
                    targets=[
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='((node_memory_SwapTotal_bytes{instance="$instance",job="$job"} - node_memory_SwapFree_bytes{instance="$instance",job="$job"}) / (node_memory_SwapTotal_bytes{instance="$instance",job="$job"})) * 100',
                            instant=True,
                            refId='A'
                        )
                    ]
                ),
                GaugePanel(
                    title='Root FS Used',
                    description='Used Root FS',
                    gridPos=GridPos(h=4, w=3, x=15, y=1),
                    format='percent',
                    decimals=1,
                    min=0,
                    max=100,
                    thresholdType='absolute',
                    thresholds=[
                        {"color": "rgba(50, 172, 45, 0.97)", "value": None},
                        {"color": "rgba(237, 129, 40, 0.89)", "value": 80},
                        {"color": "rgba(245, 54, 54, 0.9)", "value": 90}
                    ],
                    calc='lastNotNull',
                    targets=[
                        Target(
                            datasource=PROMETHEUS_DATASOURCE_NAME,
                            expr='(\n  (node_filesystem_size_bytes{instance="$instance", job="$job", mountpoint="/", fstype!="rootfs"}\n   - node_filesystem_avail_bytes{instance="$instance", job="$job", mountpoint="/", fstype!="rootfs"})\n  / node_filesystem_size_bytes{instance="$instance", job="$job", mountpoint="/", fstype!="rootfs"}\n) * 100\n',
                            format='time_series',
                            instant=True,
                            refId='A'
                        )
                    ]
                ),
            ],
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
print(dashboard.to_json_data())
