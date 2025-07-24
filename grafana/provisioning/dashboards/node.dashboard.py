from grafanalib.core import (
    Dashboard, TimeSeries, GaugePanel,
    Target, GridPos,
    OPS_FORMAT, Templating, Template, REFRESH_ON_TIME_RANGE_CHANGE, Logs
)
from grafanalib.formatunits import BYTES_IEC, SECONDS, BYTES_SEC_IEC, PERCENT_UNIT

from common import PROMETHEUS_DATASOURCE_NAME
from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

# Color definitions for panels
CPU_BASIC_COLORS = {
    "fieldConfig": {
        "defaults": {
            "custom": {
                "fillOpacity": 30,
                "lineWidth": 1,
                "showPoints": "never"
            }
        }
    }
}

MEMORY_BASIC_COLORS = {
    "fieldConfig": {
        "defaults": {
            "custom": {
                "fillOpacity": 30,
                "lineWidth": 1,
                "showPoints": "never"
            }
        }
    }
}

wrapper = SceGrafanalibWrapper("Node Exporter")

wrapper.AddPanel(
    title="CPU Basic",
    queries=[
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="system"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Busy System"
        ),
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="user"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Busy User"
        ),
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="iowait"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Busy Iowait"
        ),
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode=~".*irq"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Busy IRQs"
        ),
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job",  mode!="idle",mode!="user",mode!="system",mode!="iowait",mode!="irq",mode!="softirq"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Busy Other"
        ),
        ExpressionAndLegendPair(
            'sum(irate(node_cpu_seconds_total{instance="$instance",job="$job", mode="idle"}[$__rate_interval])) / scalar(count(count(node_cpu_seconds_total{instance="$instance",job="$job"}) by (cpu)))',
            "Idle"
        )
    ],
    unit=PERCENT_UNIT,
    dydt=False
)


wrapper.AddPanel(
    title="Memory Basic",
    queries=[
        ExpressionAndLegendPair(
            'node_memory_MemTotal_bytes{instance="$instance",job="$job"}',
            "RAM Total"
        ),
        ExpressionAndLegendPair(
            'node_memory_MemTotal_bytes{instance="$instance",job="$job"} - node_memory_MemFree_bytes{instance="$instance",job="$job"} - (node_memory_Cached_bytes{instance="$instance",job="$job"} + node_memory_Buffers_bytes{instance="$instance",job="$job"} + node_memory_SReclaimable_bytes{instance="$instance",job="$job"})',
            "RAM Used"
        ),
        ExpressionAndLegendPair(
            'node_memory_Cached_bytes{instance="$instance",job="$job"} + node_memory_Buffers_bytes{instance="$instance",job="$job"} + node_memory_SReclaimable_bytes{instance="$instance",job="$job"}',
            "RAM Cache + Buffer"
        ),
        ExpressionAndLegendPair(
            'node_memory_MemFree_bytes{instance="$instance",job="$job"}',
            "RAM Free"
        ),
        ExpressionAndLegendPair(
            '(node_memory_SwapTotal_bytes{instance="$instance",job="$job"} - node_memory_SwapFree_bytes{instance="$instance",job="$job"})',
            "SWAP Used"
        )
    ],
    unit=BYTES_IEC,
    dydt=False
)

dashboard = wrapper.Render()
