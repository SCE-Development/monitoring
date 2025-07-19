from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos

from grafanalib.formatunits import PERCENT_UNIT, SHORT, TRUE_FALSE, SECONDS, BYTES_IEC, BYTES_SEC_IEC

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair, PanelType

wrapper = SceGrafanalibWrapper(
    title="Node Exporter Full (wrapper)", panel_height=4, panel_width=3
)

# to do: potential default value for job? no data shows unless a job is selected
wrapper.DefineTemplating(
    label='Job',
    query='label_values(node_uname_info, job)',
)

wrapper.DefineTemplating(
    label='Nodename',
    query='label_values(node_uname_info{job="$job"}, nodename)',
)

wrapper.DefineTemplating(
    label='Instance',
    query='label_values(node_uname_info{job="$job", nodename="$nodename"}, instance)',
)

# to do: the panels need to have better formatting (someone may be working on this already?)
wrapper.DefineRow("Quick CPU / Mem / Disk")

wrapper.AddPanel(
    title="Pressure",
    queries=[
        ExpressionAndLegendPair(
            'irate(node_pressure_memory_waiting_seconds_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])',
        )
    ],
    unit=PERCENT_UNIT,
    panel_type_enum=PanelType.BARGAUGE,
)

wrapper.AddPanel(
    title="CPU Busy",
    queries=[
        ExpressionAndLegendPair(
            '(1 - avg(rate(' +
            'node_cpu_seconds_total{' +
            'mode="idle", instance="$instance"}' +
            '[$__rate_interval]' +
            ')))'
        )
    ],
    unit=PERCENT_UNIT,
    panel_type_enum=PanelType.GAUGE,
)

wrapper.AddPanel(
    title="Sys Load",
    queries=[
        ExpressionAndLegendPair(
            'scalar(node_load1{' +
            'instance="$instance",job="$job"}) / ' +
            'count(count(node_cpu_seconds_total{' +
            'instance="$instance",job="$job"}) ' +
            'by (cpu))'
        )
    ],
    unit=PERCENT_UNIT,
    panel_type_enum=PanelType.GAUGE,
)

wrapper.AddPanel(
    title="RAM Used",
    queries=[
        ExpressionAndLegendPair(
            '(1 - (node_memory_MemAvailable_bytes{' +
            'instance="$instance", job="$job"} / node_memory_MemTotal_bytes{' +
            'instance="$instance", job="$job"}))'
        )
    ],
    unit=PERCENT_UNIT,
    panel_type_enum=PanelType.GAUGE,
)

wrapper.AddPanel(
    title="SWAP Used",
    queries=[
        ExpressionAndLegendPair(
            '((node_memory_SwapTotal_bytes{instance="$instance",job="$job"} - ' +
            'node_memory_SwapFree_bytes{instance="$instance",job="$job"}) / ' +
            '(node_memory_SwapTotal_bytes{instance="$instance",job="$job"}))'
        )
    ],
    unit=PERCENT_UNIT,
    panel_type_enum=PanelType.GAUGE,
)

wrapper.AddPanel(
    title="Root FS Used",
    queries=[
        ExpressionAndLegendPair(
            '(\n  (node_filesystem_size_bytes{' +
            'instance="$instance", job="$job", mountpoint="/", fstype!="rootfs"' +
            '}\n   - ' +
            'node_filesystem_avail_bytes{' +
            'instance="$instance", job="$job", mountpoint="/", fstype!="rootfs"' +
            '})\n  / ' +
            'node_filesystem_size_bytes{' +
            'instance="$instance", job="$job", mountpoint="/", fstype!="rootfs"' +
            '}\n)\n'
        )
    ],
    unit=PERCENT_UNIT,
    panel_type_enum=PanelType.GAUGE,
)

wrapper.AddPanel(
    title="CPU Cores",
    queries=[
        ExpressionAndLegendPair(
            "count(count(node_cpu_seconds_total{instance=\"$instance\",job=\"$job\"}) by (cpu))",
        )
    ],
    unit=SHORT,
    panel_type_enum=PanelType.STAT,
)

wrapper.AddPanel(
    title="Reboot Required",
    queries=[
        ExpressionAndLegendPair(
            "node_reboot_required{instance=\"$instance\",job=\"$job\"}",
        )
    ],
    unit=TRUE_FALSE,
    panel_type_enum=PanelType.STAT,
)

wrapper.AddPanel(
    title="Uptime",
    queries=[
        ExpressionAndLegendPair(
            "node_time_seconds{instance=\"$instance\",job=\"$job\"} - node_boot_time_seconds{instance=\"$instance\",job=\"$job\"}",
        )
    ],
    unit=SECONDS,
    panel_type_enum=PanelType.STAT,
)

wrapper.AddPanel(
    title="RootFS Total",
    queries=[
        ExpressionAndLegendPair(
            "node_filesystem_size_bytes{instance=\"$instance\",job=\"$job\",mountpoint=\"/\",fstype!=\"rootfs\"}",
        )
    ],
    unit=BYTES_IEC,
    panel_type_enum=PanelType.STAT,
)

wrapper.AddPanel(
    title="RAM Total",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_MemTotal_bytes{instance=\"$instance\",job=\"$job\"}",
        )
    ],
    unit=BYTES_IEC,
    panel_type_enum=PanelType.STAT,
)

wrapper.AddPanel(
    title="SWAP Total",
    queries=[
        ExpressionAndLegendPair(
             "node_memory_SwapTotal_bytes{instance=\"$instance\",job=\"$job\"}",
        )
    ],
    unit=BYTES_IEC,
    panel_type_enum=PanelType.STAT,
)

wrapper.DefineRow("Basic CPU / Mem / Net / Disk")

# to do: fix coloring? (from old dashboard "# Extra JSON for the colors extraJson=CPU_BASIC_COLORS, ") , from node_consts import CPU_BASIC_COLORS, MEMORY_BASIC_COLORS
# there could be a better way to show the stacking of the panels, (can create in wrapper class in the future?)
# ex:  lineWidth=2, fillOpacity=40,  showPoints='never', stacking={'mode': 'normal'}, ... are often repeated

wrapper.DefineRow("Basic CPU / Mem / Net / Disk")

wrapper.AddPanel(
    title="CPU Basic",
    queries=[
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="system"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Busy System",
        ),
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="user"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Busy User",
        ),
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="iowait"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Busy Iowait",
        ),
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode=~".*irq"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Busy IRQs",
        ),
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job",  mode!="idle",mode!="user",mode!="system",mode!="iowait",mode!="irq",mode!="softirq"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Busy Other",
        ),
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="idle"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Idle",
        ),
    ],
    unit=PERCENT_UNIT,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory Basic",
    queries=[
        ExpressionAndLegendPair(
            'node_memory_MemTotal_bytes{instance="$instance",job="$job"}',
            "RAM Total",
        ),
        ExpressionAndLegendPair(
            'node_memory_MemTotal_bytes{instance="$instance",job="$job"} - node_memory_MemFree_bytes{instance="$instance",job="$job"} - (node_memory_Cached_bytes{instance="$instance",job="$job"} + node_memory_Buffers_bytes{instance="$instance",job="$job"} + node_memory_SReclaimable_bytes{instance="$instance",job="$job"})',
            "RAM Used",
        ),
        ExpressionAndLegendPair(
            'node_memory_Cached_bytes{instance="$instance",job="$job"} + node_memory_Buffers_bytes{instance="$instance",job="$job"} + node_memory_SReclaimable_bytes{instance="$instance",job="$job"}',
            "RAM Cache + Buffer",
        ),
        ExpressionAndLegendPair(
            'node_memory_MemFree_bytes{instance="$instance",job="$job"}',
            "RAM Free",
        ),
        ExpressionAndLegendPair(
            '(node_memory_SwapTotal_bytes{instance="$instance",job="$job"} - node_memory_SwapFree_bytes{instance="$instance",job="$job"})',
            "SWAP Used",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)          

wrapper.AddPanel(
    title="Network Traffic Basic",
    queries=[
        ExpressionAndLegendPair(
            "rate(node_network_receive_bytes_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])*8",
            "Rx {{device}}",
        ),
        ExpressionAndLegendPair(
            "-rate(node_network_transmit_bytes_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])*8",
            "Tx {{device}}",
        ),
    ],
    unit=BYTES_SEC_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
    
)

wrapper.AddPanel(
    title="Disk Space Used Basic",
    queries=[
        ExpressionAndLegendPair(
            "((node_filesystem_size_bytes{instance=\"$instance\", job=\"$job\", device!~\"rootfs\"} - node_filesystem_avail_bytes{instance=\"$instance\", job=\"$job\", device!~\"rootfs\"}) / node_filesystem_size_bytes{instance=\"$instance\", job=\"$job\", device!~\"rootfs\"}) * 100",
            "{{mountpoint}}",
        ),
    ],
    unit=PERCENT_UNIT,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

dashboard = wrapper.Render()
