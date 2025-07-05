from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair, PanelType

from grafanalib.formatunits import PERCENT_UNIT

wrapper = SceGrafanalibWrapper(
    title="Node Exporter Full (wrapper)", panel_height=4, panel_width=3
)
wrapper.DefineRow("Quick CPU / Mem / Disk")
wrapper.DefineTemplating("datasource", "Datasource", "prometheus", 'datasource')
wrapper.DefineTemplating("job", "Job", "label_values(node_uname_info, job)")
wrapper.DefineTemplating(
    "nodename", "Nodename", 'label_values(node_uname_info{job="$job"}, nodename)'
)
wrapper.DefineTemplating(
    "node",
    "Instance",
    'label_values(node_uname_info{job="$job", nodename="$nodename"}, instance)',
)
wrapper.AddPanel(
    title="CPU Busy",
    queries=[
        ExpressionAndLegendPair(
            '(1 - avg(rate(node_cpu_seconds_total{mode="idle", instance="$node"}[$__rate_interval])))'
        )
    ],
    unit=PERCENT_UNIT,
    panel_type_enum=PanelType.GAUGE,
)
wrapper.AddPanel(
    title="Sys Load",
    queries=[
        ExpressionAndLegendPair(
            'scalar(node_load1{instance="$node",job="$job"}) / count(count(node_cpu_seconds_total{instance="$node",job="$job"}) by (cpu))'
        )
    ],
    unit=PERCENT_UNIT,
    panel_type_enum=PanelType.GAUGE,
)
wrapper.AddPanel(
    title="RAM Used",
    queries=[
        ExpressionAndLegendPair(
            '(1 - (node_memory_MemAvailable_bytes{instance="$node", job="$job"} / node_memory_MemTotal_bytes{instance="$node", job="$job"}))'
        )
    ],
    unit=PERCENT_UNIT,
    panel_type_enum=PanelType.GAUGE,
)
wrapper.AddPanel(
    title="SWAP Used",
    queries=[
        ExpressionAndLegendPair(
            '((node_memory_SwapTotal_bytes{instance="$node",job="$job"} - node_memory_SwapFree_bytes{instance="$node",job="$job"}) / (node_memory_SwapTotal_bytes{instance="$node",job="$job"}))'
        )
    ],
    unit=PERCENT_UNIT,
    panel_type_enum=PanelType.GAUGE,
)
wrapper.AddPanel(
    title="Root FS Used",
    queries=[
        ExpressionAndLegendPair(
            '(\n  (node_filesystem_size_bytes{instance="$node", job="$job", mountpoint="/", fstype!="rootfs"}\n   - node_filesystem_avail_bytes{instance="$node", job="$job", mountpoint="/", fstype!="rootfs"})\n  / node_filesystem_size_bytes{instance="$node", job="$job", mountpoint="/", fstype!="rootfs"}\n)\n'
        )
    ],
    unit=PERCENT_UNIT,
    panel_type_enum=PanelType.GAUGE,
)
dashboard = wrapper.Render()
