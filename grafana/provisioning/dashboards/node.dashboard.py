from grafanalib.core import Dashboard, Templating, Template, TimeSeries, GridPos, Target, Row, GaugePanel
from grafanalib.formatunits import BYTES_IEC, PERCENT_UNIT, BYTES_SEC_IEC

PROMETHEUS_DATASOURCE_NAME = 'Prometheus'
from node_consts import CPU_BASIC_COLORS, MEMORY_BASIC_COLORS, GAUGE_CONFIGS, TIMESERIES_CONFIGS 

def create_timeseries_panel(config):
    """Create a TimeSeries panel from a configuration dictionary."""
    return TimeSeries(
        title=config['title'],
        description=config.get('description', ''),
        unit=config['unit'],
        gridPos=GridPos(h=8, w=12, x=config['x_pos'], y=config.get('y_pos', 0)),
        lineWidth=config.get('lineWidth', 1),
        fillOpacity=config.get('fillOpacity', 30),
        showPoints='never',
        stacking=config.get('stacking', {'mode': 'none'}),
        tooltipMode='all',
        tooltipSort='desc',
        targets=[Target(**target) for target in config['targets']],
        extraJson=config.get('extraJson', {})
    )

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
            panels=[create_timeseries_panel(config) for config in TIMESERIES_CONFIGS],
        )
    ]
).auto_panel_ids()
