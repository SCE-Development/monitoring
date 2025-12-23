from grafanalib.core import Dashboard, Templating, Template, TimeSeries, Target, GridPos
from grafanalib.formatunits import SECONDS

from wrapper import SceGrafanalibWrapper, ExpressionAndLegendPair

wrapper = SceGrafanalibWrapper(title='sign2')

wrapper.AddPanel(
    title="Sign last updated",
    queries=[
        ExpressionAndLegendPair(
            'time() - sign_last_updated{job="SCE-sign2"}',
        ),
    ],
    unit=SECONDS
)

wrapper.AddPanel(
    title="Sign update error",
    queries=[
        ExpressionAndLegendPair(
            'sign_update_error{job="SCE-sign2"}'
        )
 ],
)

wrapper.AddPanel(
    title="LeetCode API Error",
    queries=[
        ExpressionAndLegendPair(
            'leetcode_api_error{job="SCE-sign2"}'
        )
 ],
)

wrapper.AddPanel(
    title="Endpoint hits",
    queries=[
        ExpressionAndLegendPair(
            'endpoint_hits_total{job="SCE-sign2", path!~"/metrics|.*[.].*"}',
            "{{code}} {{path}}",
        )
    ],
)

wrapper.AddPanel(
    title="LeetCode API Response Codes",
    queries=[
        ExpressionAndLegendPair(
            'leetcode_api_response_codes_total{job="SCE-sign2"}',
            "{{code}}",
        )
    ],
)

wrapper.AddPanel(
    title="LeetCode API latency",
    queries=[
        ExpressionAndLegendPair(
            'leetcode_api_latency_sum / leetcode_api_latency_count{job="SCE-sign2"}',
        )
    ],
)

wrapper.AddPanel(
    title="Container Uptime",
    queries=[
        ExpressionAndLegendPair(
            'time() - process_start_time_seconds{job="SCE-sign2"}',
        )
    ],
    unit=SECONDS
)

wrapper.AddPanel(
    title="WAV Last Sent",
    queries=[
        ExpressionAndLegendPair(
            'time() - wav_last_sent{job="SCE-sign2"}',
        )
    ],
    unit=SECONDS
)

wrapper.AddPanel(
    title="WAV Last Generated",
    queries=[
        ExpressionAndLegendPair(
            'time() - wav_last_generated{job="SCE-sign2"}',
        )
    ],
    unit=SECONDS
)

wrapper.AddPanel(
    title="Custom Metric (SECONDS)",
    queries=[
        ExpressionAndLegendPair(
            'custom_metric_seconds{job="SCE-sign2"}',
        ),
    ],
    unit=SECONDS
)

dashboard = wrapper.Render()
