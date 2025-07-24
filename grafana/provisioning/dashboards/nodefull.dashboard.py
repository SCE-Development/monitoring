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

stat_panels = [
    ("CPU Cores", "count(count(node_cpu_seconds_total{instance=\"$instance\",job=\"$job\"}) by (cpu))", SHORT),
    ("Reboot Required", "node_reboot_required{instance=\"$instance\",job=\"$job\"}", TRUE_FALSE),
    ("Uptime", "node_time_seconds{instance=\"$instance\",job=\"$job\"} - node_boot_time_seconds{instance=\"$instance\",job=\"$job\"}", SECONDS),
    ("RootFS Total", "node_filesystem_size_bytes{instance=\"$instance\",job=\"$job\",mountpoint=\"/\",fstype!=\"rootfs\"}", BYTES_IEC),
    ("RAM Total", "node_memory_MemTotal_bytes{instance=\"$instance\",job=\"$job\"}", BYTES_IEC),
    ("SWAP Total", "node_memory_SwapTotal_bytes{instance=\"$instance\",job=\"$job\"}", BYTES_IEC),
]

for title, query, unit in stat_panels:
    wrapper.AddPanel(
        title=title,
        queries=[
            ExpressionAndLegendPair(query)
        ],
        unit=unit,
        panel_type_enum=PanelType.STAT,
    )

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

# doesnt have calcs yet, ex: "calcs": [ "min", "mean","max", "lastNotNull" ],
# may need more custom stacking as well? 

wrapper.DefineRow("CPU / Mem / Net / Disk")

wrapper.AddPanel(
    title="CPU",
    queries=[
        ExpressionAndLegendPair(
            "sum(irate(node_cpu_seconds_total{mode=\"system\",instance=\"$instance\",job=\"$job\"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance=\"$instance\",job=\"$job\"}) by (cpu)))",
            "System - Processes executing in kernel mode",
        ),
        ExpressionAndLegendPair(
            "sum(irate(node_cpu_seconds_total{mode=\"user\",instance=\"$instance\",job=\"$job\"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance=\"$instance\",job=\"$job\"}) by (cpu)))",
            "User - Normal processes executing in user mode",
        ),
        ExpressionAndLegendPair(
            "sum(irate(node_cpu_seconds_total{mode=\"nice\",instance=\"$instance\",job=\"$job\"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance=\"$instance\",job=\"$job\"}) by (cpu)))",
            "Nice - Niced processes executing in user mode",
        ),
        ExpressionAndLegendPair(
            "sum(irate(node_cpu_seconds_total{mode=\"iowait\",instance=\"$instance\",job=\"$job\"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance=\"$instance\",job=\"$job\"}) by (cpu)))",
            "Iowait - Waiting for I/O to complete",
        ),
        ExpressionAndLegendPair(
            "sum(irate(node_cpu_seconds_total{mode=\"irq\",instance=\"$instance\",job=\"$job\"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance=\"$instance\",job=\"$job\"}) by (cpu)))",
            "Irq - Servicing interrupts",
        ),
        ExpressionAndLegendPair(
            "sum(irate(node_cpu_seconds_total{mode=\"softirq\",instance=\"$instance\",job=\"$job\"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance=\"$instance\",job=\"$job\"}) by (cpu)))",
            "Softirq - Servicing softirqs",
        ),
        ExpressionAndLegendPair(
            "sum(irate(node_cpu_seconds_total{mode=\"steal\",instance=\"$instance\",job=\"$job\"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance=\"$instance\",job=\"$job\"}) by (cpu)))",
            "Steal - Time spent in other operating systems when running in a virtualized environment",
        ),
        ExpressionAndLegendPair(
            "sum(irate(node_cpu_seconds_total{mode=\"idle\",instance=\"$instance\",job=\"$job\"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance=\"$instance\",job=\"$job\"}) by (cpu)))",
            "Idle - Waiting for something to happen",

        ),
        ExpressionAndLegendPair(
            "sum by(instance) (irate(node_cpu_guest_seconds_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])) / on(instance) group_left sum by (instance)((irate(node_cpu_seconds_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval]))) > 0",
            "Guest CPU usage",
        ),
    ],
    unit=PERCENT_UNIT,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_MemTotal_bytes{instance=\"$instance\",job=\"$job\"} - node_memory_MemFree_bytes{instance=\"$instance\",job=\"$job\"} - node_memory_Buffers_bytes{instance=\"$instance\",job=\"$job\"} - node_memory_Cached_bytes{instance=\"$instance\",job=\"$job\"} - node_memory_Slab_bytes{instance=\"$instance\",job=\"$job\"} - node_memory_PageTables_bytes{instance=\"$instance\",job=\"$job\"} - node_memory_SwapCached_bytes{instance=\"$instance\",job=\"$job\"}",
            "Apps - Memory used by user-space applications",
        ),
        ExpressionAndLegendPair(
            "node_memory_PageTables_bytes{instance=\"$instance\",job=\"$job\"}",
            "PageTables - Memory used to map between virtual and physical memory addresses",
        ),
        ExpressionAndLegendPair(
            "node_memory_SwapCached_bytes{instance=\"$instance\",job=\"$job\"}",
            "SwapCache - Memory that keeps track of pages that have been fetched from swap but not yet been modified",
        ),
        ExpressionAndLegendPair(
            "node_memory_Slab_bytes{instance=\"$instance\",job=\"$job\"}",
            "Slab - Memory used by the kernel to cache data structures for its own use (caches like inode, dentry, etc)",
        ),
        ExpressionAndLegendPair(
            "node_memory_Cached_bytes{instance=\"$instance\",job=\"$job\"}",
            "Cache - Parked file data (file content) cache",
        ),
        ExpressionAndLegendPair(
            "node_memory_Buffers_bytes{instance=\"$instance\",job=\"$job\"}",
            "Buffers - Block device (e.g. harddisk) cache",
        ),
        ExpressionAndLegendPair(
            "node_memory_MemFree_bytes{instance=\"$instance\",job=\"$job\"}",
            "Unused - Free memory unassigned",
        ),
        ExpressionAndLegendPair(
            "(node_memory_SwapTotal_bytes{instance=\"$instance\",job=\"$job\"} - node_memory_SwapFree_bytes{instance=\"$instance\",job=\"$job\"})",
            "Swap - Swap space used",
        ),
        ExpressionAndLegendPair(
            "node_memory_HardwareCorrupted_bytes{instance=\"$instance\",job=\"$job\"}",
            "Hardware Corrupted - Amount of RAM that the kernel identified as corrupted / not working",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)
            
wrapper.AddPanel(
    title="Network Traffic",
    queries=[
        ExpressionAndLegendPair(
            "(rate(node_network_receive_bytes_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])\n / ignoring(speed) node_network_speed_bytes{instance=\"$instance\",job=\"$job\", speed!=\"-1\"}) * 100",
            "{{device}} - Rx in",
        ),
        ExpressionAndLegendPair(
            "-(rate(node_network_transmit_bytes_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])\n / ignoring(speed) node_network_speed_bytes{instance=\"$instance\",job=\"$job\", speed!=\"-1\"}) * 100",
            "{{device}} - Tx out",
        ),
    ],
    unit=BYTES_SEC_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Network Saturation",
    queries=[
        ExpressionAndLegendPair(
            "(rate(node_network_receive_bytes_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])\n / ignoring(speed) node_network_speed_bytes{instance=\"$instance\",job=\"$job\", speed!=\"-1\"}) * 100",
            "{{device}} - Rx in",
        ),
        ExpressionAndLegendPair(
            "-(rate(node_network_transmit_bytes_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])\n / ignoring(speed) node_network_speed_bytes{instance=\"$instance\",job=\"$job\", speed!=\"-1\"}) * 100",
              "{{device}} - Tx out",
        ),
    ],
    unit=PERCENT_UNIT,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Disk IOps",
    queries=[
        ExpressionAndLegendPair(
            "irate(node_disk_reads_completed_total{instance=\"$instance\",job=\"$job\",device=~\"$diskdevices\"}[$__rate_interval])",
            "{{device}} - Read",
        ),
        ExpressionAndLegendPair(
            "irate(node_disk_writes_completed_total{instance=\"$instance\",job=\"$job\",device=~\"$diskdevices\"}[$__rate_interval])",
            "{{device}} - Write",
        ),
    ],
    unit='io/s',
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Disk Throughput",
    queries=[
        ExpressionAndLegendPair(
            "irate(node_disk_read_bytes_total{instance=\"$instance\",job=\"$job\",device=~\"$diskdevices\"}[$__rate_interval])",
            "{{device}} - Read",
        ),
        ExpressionAndLegendPair(
            "irate(node_disk_written_bytes_total{instance=\"$instance\",job=\"$job\",device=~\"$diskdevices\"}[$__rate_interval])",
            "{{device}} - Write",
        ),
    ],
    unit=PERCENT_UNIT,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)         
            
wrapper.AddPanel(
    title="Filesystem Space Available",
    queries=[
        ExpressionAndLegendPair(
            "node_filesystem_avail_bytes{instance=\"$instance\",job=\"$job\",device!~'rootfs'}",
            "{{mountpoint}}",
        ),
        ExpressionAndLegendPair(
            "node_filesystem_free_bytes{instance=\"$instance\",job=\"$job\",device!~'rootfs'}",
            "{{mountpoint}} - Free",
        ),
        ExpressionAndLegendPair(
            "node_filesystem_size_bytes{instance=\"$instance\",job=\"$job\",device!~'rootfs'}",
            "{{mountpoint}} - Size",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Filesystem Used",
    queries=[
        ExpressionAndLegendPair(
            "node_filesystem_size_bytes{instance=\"$instance\",job=\"$job\",device!~'rootfs'} - node_filesystem_avail_bytes{instance=\"$instance\",job=\"$job\",device!~'rootfs'}",
            "{{mountpoint}}",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)
            
wrapper.AddPanel(
    title="Disk I/O Utilization",
    queries=[
        ExpressionAndLegendPair(
            "irate(node_disk_io_time_seconds_total{instance=\"$instance\",job=\"$job\",device=~\"$diskdevices\"} [$__rate_interval])",
            "{{device}}",
        ),
    ],
    unit=PERCENT_UNIT,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Pressure Stall Information",
    queries=[
        ExpressionAndLegendPair(
            "rate(node_pressure_cpu_waiting_seconds_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "CPU - Some",
        ),
        ExpressionAndLegendPair(
            "rate(node_pressure_memory_waiting_seconds_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "Memory - Some",
        ),
        ExpressionAndLegendPair(
            "rate(node_pressure_memory_stalled_seconds_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "Memory - Full",
        ),
        ExpressionAndLegendPair(
            "rate(node_pressure_io_waiting_seconds_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "I/O - Some",
        ),
        ExpressionAndLegendPair(
            "rate(node_pressure_io_stalled_seconds_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "I/O - Full",
        ),
        ExpressionAndLegendPair(
            "rate(node_pressure_irq_stalled_seconds_total{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "IRQ - Full",
        ),
    ],
    unit=PERCENT_UNIT,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.DefineRow("Memory Meminfo")

wrapper.AddPanel(
    title="Memory Committed",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_Committed_AS_bytes{instance=\"$instance\",job=\"$job\"}",
            "Committed_AS - Memory promised to processes (not necessarily used)",
        ),
        ExpressionAndLegendPair(
            "node_memory_CommitLimit_bytes{instance=\"$instance\",job=\"$job\"}", 
            "CommitLimit - Max allowable committed memory",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory Writeback and Dirty",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_Writeback_bytes{instance=\"$instance\",job=\"$job\"}",
            "Writeback - Memory currently being flushed to disk",
        ),
        ExpressionAndLegendPair(
            "node_memory_WritebackTmp_bytes{instance=\"$instance\",job=\"$job\"}",
            "WritebackTmp - FUSE temporary writeback buffers",
        ),
        ExpressionAndLegendPair(
            "node_memory_Dirty_bytes{instance=\"$instance\",job=\"$job\"}",
            "Dirty - Memory marked dirty (pending write to disk)",
        ),
        ExpressionAndLegendPair(
            "node_memory_NFS_Unstable_bytes{instance=\"$instance\",job=\"$job\"}",
            "NFS Unstable - Pages sent to NFS server, awaiting storage commit",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory Slab",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_SUnreclaim_bytes{instance=\"$instance\",job=\"$job\"}",
            "SUnreclaim - Non-reclaimable slab memory (kernel objects)",
        ),
        ExpressionAndLegendPair(
            "node_memory_SReclaimable_bytes{instance=\"$instance\",job=\"$job\"}",
            "SReclaimable - Potentially reclaimable slab memory (e.g., inode cache)",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory Shared and Mapped",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_Mapped_bytes{instance=\"$instance\",job=\"$job\"}",
            "Mapped - Memory mapped from files (e.g., libraries, mmap)",
        ),
        ExpressionAndLegendPair(
            "node_memory_Shmem_bytes{instance=\"$instance\",job=\"$job\"}",
            "Shmem - Shared memory used by processes and tmpfs",
        ),
        ExpressionAndLegendPair(
            "node_memory_ShmemHugePages_bytes{instance=\"$instance\",job=\"$job\"}",
            "ShmemHugePages - Shared memory (shmem/tmpfs) allocated with HugePages",
        ),
        ExpressionAndLegendPair(
            "node_memory_ShmemPmdMapped_bytes{instance=\"$instance\",job=\"$job\"}",
            "PMD Mapped - Shmem/tmpfs backed by Transparent HugePages (PMD)",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory LRU Active / Inactive (%)",
    queries=[
        ExpressionAndLegendPair(
            "(node_memory_Inactive_bytes{instance=\"$instance\",job=\"$job\"}) \n/ \n(node_memory_MemTotal_bytes{instance=\"$instance\",job=\"$job\"})",
            "Inactive - Less recently used memory, more likely to be reclaimed",
        ),
        ExpressionAndLegendPair(
            "(node_memory_Active_bytes{instance=\"$instance\",job=\"$job\"}) \n/ \n(node_memory_MemTotal_bytes{instance=\"$instance\",job=\"$job\"})\n",
            "Active - Recently used memory, retained unless under pressure",
        ),
    ],
    unit=PERCENT_UNIT,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)
              
wrapper.AddPanel(
    title="Memory LRU Active / Inactive Detail",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_Inactive_file_bytes{instance=\"$instance\",job=\"$job\"}",
            "Inactive_file - File-backed memory on inactive LRU list",
        ),
        ExpressionAndLegendPair(
            "node_memory_Inactive_anon_bytes{instance=\"$instance\",job=\"$job\"}",
            "Inactive_anon - Anonymous memory on inactive LRU (incl. tmpfs & swap cache)",
        ),
        ExpressionAndLegendPair(
            "node_memory_Active_file_bytes{instance=\"$instance\",job=\"$job\"}",
            "Active_file - File-backed memory on active LRU list",
        ),
        ExpressionAndLegendPair(
            "node_memory_Active_anon_bytes{instance=\"$instance\",job=\"$job\"}",
            "Active_anon - Anonymous memory on active LRU (incl. tmpfs & swap cache)",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory Kernel / CPU / IO",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_KernelStack_bytes{instance=\"$instance\",job=\"$job\"}",
            "KernelStack - Kernel stack memory (per-thread, non-reclaimable)",
        ),
        ExpressionAndLegendPair(
            "node_memory_Percpu_bytes{instance=\"$instance\",job=\"$job\"}",
            "PerCPU - Dynamically allocated per-CPU memory (used by kernel modules)",
        ),
        ExpressionAndLegendPair(
            "node_memory_Bounce_bytes{instance=\"$instance\",job=\"$job\"}",
            "Bounce Memory - I/O buffer for DMA-limited devices",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory Vmalloc",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_VmallocChunk_bytes{instance=\"$instance\",job=\"$job\"}",
            "Vmalloc Free Chunk - Largest available block in vmalloc area",
        ),
        ExpressionAndLegendPair(
            "node_memory_VmallocTotal_bytes{instance=\"$instance\",job=\"$job\"}",
            "Vmalloc Total - Total size of the vmalloc memory area",
        ),
        ExpressionAndLegendPair(
            "node_memory_VmallocUsed_bytes{instance=\"$instance\",job=\"$job\"}",
            "Vmalloc Used - Portion of vmalloc area currently in use",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory Anonymous",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_AnonHugePages_bytes{instance=\"$instance\",job=\"$job\"}",
            "AnonHugePages - Anonymous memory using HugePages",
        ),
        ExpressionAndLegendPair(
            "node_memory_AnonPages_bytes{instance=\"$instance\",job=\"$job\"}",
            "AnonPages - Anonymous memory (non-file-backed)",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory Unevicatble and MLocked",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_Unevictable_bytes{instance=\"$instance\",job=\"$job\"}",
            "Unevictable - Kernel-pinned memory (not swappable)",
        ),
        ExpressionAndLegendPair(
            "node_memory_Mlocked_bytes{instance=\"$instance\",job=\"$job\"}",
            "Mlocked - Application-locked memory via mlock()",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory DirectMap",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_DirectMap1G_bytes{instance=\"$instance\",job=\"$job\"}",
            "DirectMap 1G - Memory mapped with 1GB pages",
        ),
        ExpressionAndLegendPair(
            "node_memory_DirectMap2M_bytes{instance=\"$instance\",job=\"$job\"}",
            "DirectMap 2M - Memory mapped with 2MB pages",
        ),
        ExpressionAndLegendPair(
            "node_memory_DirectMap4k_bytes{instance=\"$instance\",job=\"$job\"}",
            "DirectMap 4K - Memory mapped with 4KB pages",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory HugePages",
    queries=[
        ExpressionAndLegendPair(
            "node_memory_HugePages_Free{instance=\"$instance\",job=\"$job\"} * node_memory_Hugepagesize_bytes{instance=\"$instance\",job=\"$job\"}",
            "HugePages Used - Currently allocated",
        ),
        ExpressionAndLegendPair(
            "node_memory_HugePages_Rsvd{instance=\"$instance\",job=\"$job\"} * node_memory_Hugepagesize_bytes{instance=\"$instance\",job=\"$job\"}",
            "HugePages Reserved - Promised but unused",
        ),
        ExpressionAndLegendPair(
            "node_memory_HugePages_Surp{instance=\"$instance\",job=\"$job\"} * node_memory_Hugepagesize_bytes{instance=\"$instance\",job=\"$job\"}",
            "HugePages Surplus - Dynamic pool extension",
        ),
        ExpressionAndLegendPair(
            "node_memory_HugePages_Total{instance=\"$instance\",job=\"$job\"} * node_memory_Hugepagesize_bytes{instance=\"$instance\",job=\"$job\"}",
            "HugePages Total - Reserved memory",
        ),
    ],
    unit=BYTES_IEC,
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.DefineRow("Memory Vmstat")

wrapper.AddPanel(
    title="Memory Pages In / Out",
    queries=[
        ExpressionAndLegendPair(
            "irate(node_vmstat_pgpgin{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "Pagesin - Page in ops",
        ),
        ExpressionAndLegendPair(
            "irate(node_vmstat_pgpgout{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "Pagesout - Page out ops",
        ),
    ],
    unit='ops',
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory Pages Swap In / Out",
    queries=[
        ExpressionAndLegendPair(
            "irate(node_vmstat_pswpin{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "Pswpin - Pages swapped in",
        ),
        ExpressionAndLegendPair(
            "irate(node_vmstat_pswpout{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "Pswpout - Pages swapped out",
        ),
    ],
    unit='ops',
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="Memory Page Faults",
    queries=[
        ExpressionAndLegendPair(
            "irate(node_vmstat_pgfault{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "Pgfault - Page major and minor fault ops",
        ),
        ExpressionAndLegendPair(
            "irate(node_vmstat_pgmajfault{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "Pgmajfault - Major page fault ops",
        ),
        ExpressionAndLegendPair(
            "irate(node_vmstat_pgfault{instance=\"$node\",job=\"$job\"}[$__rate_interval])  - irate(node_vmstat_pgmajfault{instance=\"$node\",job=\"$job\"}[$__rate_interval])",
            "Pgminfault - Minor page fault ops",
        ),
    ],
    unit='ops',
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

wrapper.AddPanel(
    title="OOM Killer",
    queries=[
        ExpressionAndLegendPair(
            "irate(node_vmstat_oom_kill{instance=\"$instance\",job=\"$job\"}[$__rate_interval])",
            "OOM Kills",
        ),
    ],
    unit='ops',
    lineWidth=2,
    fillOpacity=40,
    showPoints='never',
    stacking={'mode': 'normal'},
)

dashboard = wrapper.Render()
